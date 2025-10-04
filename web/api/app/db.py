from __future__ import annotations

import socket
from contextlib import contextmanager
from typing import Iterator

import psycopg2
from loguru import logger

from .config import get_settings


@contextmanager
def admin_connection(autocommit: bool = False) -> Iterator[psycopg2.extensions.connection]:
    settings = get_settings()
    conn = psycopg2.connect(
        host=_resolve_host(settings.db_host),
        port=settings.db_port,
        dbname=settings.db_name,
        user=settings.db_admin_user,
        password=settings.db_admin_password,
    )
    try:
        conn.autocommit = autocommit
        yield conn
    finally:
        conn.close()


@contextmanager
def restricted_connection(autocommit: bool = False) -> Iterator[psycopg2.extensions.connection]:
    settings = get_settings()
    conn = psycopg2.connect(
        host=_resolve_host(settings.db_host),
        port=settings.db_port,
        dbname=settings.db_name,
        user=settings.db_web_user,
        password=settings.db_web_password,
    )
    try:
        conn.autocommit = autocommit
        yield conn
    finally:
        conn.close()


def _resolve_host(host: str) -> str:
    try:
        socket.getaddrinfo(host, None)
        return host
    except socket.gaierror:
        fallback = "127.0.0.1"
        logger.warning("Database host '%s' could not be resolved; falling back to %s", host, fallback)
        return fallback
