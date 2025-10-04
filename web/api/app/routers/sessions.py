from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException, Response, status

from ..schemas import (
    ChallengeSchemaTable,
    SessionCreateResponse,
    SessionResetRequest,
)
from ..services import sessions as session_service

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("", response_model=SessionCreateResponse, status_code=201)
def create_session() -> SessionCreateResponse:
    session_id = session_service.create_session()
    return SessionCreateResponse(session_id=session_id)


@router.post("/{session_id}/reset", status_code=204)
def reset_session(session_id: UUID, payload: SessionResetRequest) -> Response:
    try:
        session_service.reset_session_schema(session_id, payload.challenge_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{session_id}/schema", response_model=list[ChallengeSchemaTable])
def session_schema(session_id: UUID) -> list[ChallengeSchemaTable]:
    try:
        return session_service.get_schema_overview(session_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
