from __future__ import annotations

import os
from typing import Dict, List, Optional, Tuple
from uuid import UUID, uuid4

from loguru import logger
from psycopg2 import sql

from ..config import get_settings
from ..db import admin_connection, restricted_connection
from ..schemas import ChallengeSchemaColumn, ChallengeSchemaTable
from .challenges import resolve_challenge_path


def _generate_schema_name(session_id: UUID) -> str:
    settings = get_settings()
    return f"{settings.session_schema_prefix}{session_id.hex}"


def create_session() -> UUID:
    session_id = uuid4()
    schema_name = _generate_schema_name(session_id)

    with admin_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO web_sessions (session_id, schema_name, created_at, last_active)
                VALUES (%s, %s, NOW(), NOW())
                ON CONFLICT (session_id) DO UPDATE
                SET schema_name = EXCLUDED.schema_name,
                    last_active = NOW()
                """,
                (str(session_id), schema_name),
            )
            cur.execute(sql.SQL("DROP SCHEMA IF EXISTS {} CASCADE").format(sql.Identifier(schema_name)))
            cur.execute(sql.SQL("CREATE SCHEMA {} AUTHORIZATION {};").format(
                sql.Identifier(schema_name),
                sql.Identifier(get_settings().db_admin_user),
            ))
            conn.commit()

    logger.info("Created session {} with schema {}", session_id, schema_name)
    return session_id


def _fetch_schema_name(session_id: UUID) -> str:
    with admin_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT schema_name FROM web_sessions WHERE session_id = %s",
                (str(session_id),),
            )
            row = cur.fetchone()
            if not row:
                raise KeyError(f"Session not found: {session_id}")
            return row[0]


def _touch_session(session_id: UUID) -> None:
    with admin_connection(autocommit=True) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE web_sessions SET last_active = NOW() WHERE session_id = %s",
                (str(session_id),),
            )


def reset_session_schema(session_id: UUID, challenge_id: str) -> None:
    schema_name = _fetch_schema_name(session_id)
    challenge_dir = resolve_challenge_path(challenge_id)
    settings = get_settings()

    with admin_connection() as conn:
        with conn.cursor() as cur:
            logger.info("Resetting schema {} for session {}", schema_name, session_id)
            cur.execute(sql.SQL("DROP SCHEMA IF EXISTS {} CASCADE").format(sql.Identifier(schema_name)))
            cur.execute(sql.SQL("CREATE SCHEMA {} AUTHORIZATION {};").format(
                sql.Identifier(schema_name),
                sql.Identifier(settings.db_admin_user),
            ))
            cur.execute(
                """
                UPDATE web_sessions
                SET last_active = NOW()
                WHERE session_id = %s
                """,
                (str(session_id),),
            )

            # Execute each setup SQL file inside the new schema
            setup_files = []
            challenge_yaml_dir = challenge_dir
            challenge_definition_path = os.path.join(challenge_yaml_dir, "challenge.yaml")
            import yaml

            with open(challenge_definition_path, "r", encoding="utf-8") as f:
                challenge_definition = yaml.safe_load(f)

            for setup_entry in challenge_definition.get("setup", []):
                file_path = os.path.join(challenge_yaml_dir, setup_entry.get("file"))
                if os.path.exists(file_path):
                    setup_files.append(file_path)
                else:
                    raise FileNotFoundError(f"Setup file missing: {file_path}")

            cur.execute(sql.SQL("SET search_path TO {};").format(sql.Identifier(schema_name)))
            for file_path in setup_files:
                with open(file_path, "r", encoding="utf-8") as setup_file:
                    sql_script = setup_file.read()
                cur.execute(sql.SQL("SET search_path TO {};").format(sql.Identifier(schema_name)))
                cur.execute(sql_script)

            restricted_role = settings.db_web_user
            cur.execute(sql.SQL("GRANT USAGE ON SCHEMA {} TO {};").format(
                sql.Identifier(schema_name),
                sql.Identifier(restricted_role),
            ))
            cur.execute(sql.SQL("GRANT SELECT ON ALL TABLES IN SCHEMA {} TO {};").format(
                sql.Identifier(schema_name),
                sql.Identifier(restricted_role),
            ))
            cur.execute(sql.SQL("GRANT SELECT ON ALL SEQUENCES IN SCHEMA {} TO {};").format(
                sql.Identifier(schema_name),
                sql.Identifier(restricted_role),
            ))
            cur.execute(sql.SQL("ALTER DEFAULT PRIVILEGES IN SCHEMA {} GRANT SELECT ON TABLES TO {};").format(
                sql.Identifier(schema_name),
                sql.Identifier(restricted_role),
            ))
            conn.commit()

    logger.info("Prepared challenge {} for session {} in schema {}", challenge_id, session_id, schema_name)


def _set_search_path(cursor, schema_name: str) -> None:
    cursor.execute(sql.SQL("SET search_path TO {};").format(sql.Identifier(schema_name)))


def execute_user_sql(session_id: UUID, query: str) -> Tuple[List[str], List[List[Optional[str]]]]:
    schema_name = _fetch_schema_name(session_id)
    settings = get_settings()

    with restricted_connection() as conn:
        with conn.cursor() as cur:
            _set_search_path(cur, schema_name)
            cur.execute("SET LOCAL statement_timeout = %s;", (settings.statement_timeout_ms,))
            cur.execute(query)

            if cur.description:
                columns = [col.name for col in cur.description]
                rows = cur.fetchmany(settings.max_result_rows)
                conn.rollback()
                _touch_session(session_id)
                return columns, [
                    [None if value is None else str(value) for value in row]
                    for row in rows
                ]
            conn.rollback()
            _touch_session(session_id)
            return [], []


def get_schema_overview(session_id: UUID) -> List[ChallengeSchemaTable]:
    schema_name = _fetch_schema_name(session_id)
    tables: Dict[str, List[ChallengeSchemaColumn]] = {}

    with admin_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT table_name, column_name, data_type
                FROM information_schema.columns
                WHERE table_schema = %s
                ORDER BY table_name, ordinal_position
                """,
                (schema_name,),
            )
            for table_name, column_name, data_type in cur.fetchall():
                tables.setdefault(table_name, []).append(
                    ChallengeSchemaColumn(name=column_name, data_type=data_type)
                )

    _touch_session(session_id)

    return [
        ChallengeSchemaTable(table_name=table, columns=cols)
        for table, cols in tables.items()
    ]


def validate_solution(session_id: UUID, challenge_id: str, user_sql: str) -> Tuple[bool, str]:
    schema_name = _fetch_schema_name(session_id)
    challenge_dir = resolve_challenge_path(challenge_id)

    import yaml
    from pokedex import validator, db as cli_db

    challenge_yaml_path = os.path.join(challenge_dir, "challenge.yaml")
    with open(challenge_yaml_path, "r", encoding="utf-8") as f:
        challenge_definition = yaml.safe_load(f)

    with admin_connection() as conn:
        conn.autocommit = False
        with conn.cursor() as cur:
            _set_search_path(cur, schema_name)
        try:
            success, message = validator.run_validation(conn, challenge_definition, user_sql, cli_db)
            conn.rollback()
            _touch_session(session_id)
            return success, message
        finally:
            conn.rollback()
