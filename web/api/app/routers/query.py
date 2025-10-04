from __future__ import annotations

import time
from uuid import UUID

from fastapi import APIRouter, HTTPException
from psycopg2 import Error as PsycopgError

from ..schemas import QueryRequest, QueryResponse, QueryResult, ValidationDetail
from ..services import sessions
from ..services.limits import RateLimitExceeded, enforce_rate_limit

router = APIRouter(prefix="/sessions", tags=["query"])


@router.post("/{session_id}/query", response_model=QueryResponse)
def execute_query(session_id: UUID, payload: QueryRequest) -> QueryResponse:
    if not payload.sql.strip():
        raise HTTPException(status_code=400, detail="SQL query cannot be empty")

    try:
        enforce_rate_limit(str(session_id))
    except RateLimitExceeded as exc:
        raise HTTPException(status_code=429, detail=str(exc)) from exc

    start = time.perf_counter()
    try:
        columns, rows = sessions.execute_user_sql(session_id, payload.sql)
    except PsycopgError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    elapsed_ms = (time.perf_counter() - start) * 1000
    result = QueryResult(
        columns=columns,
        rows=rows,
        row_count=len(rows),
        execution_time_ms=elapsed_ms,
    )

    validation = None
    if payload.validate_result and payload.challenge_id:
        try:
            success, message = sessions.validate_solution(session_id, payload.challenge_id, payload.sql)
            validation = ValidationDetail(success=success, message=message)
        except PsycopgError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    return QueryResponse(result=result, validation=validation)
