from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..schemas import ChallengeDetail, ChallengeListResponse
from ..services import challenges as challenge_service

router = APIRouter(prefix="/challenges", tags=["challenges"])


@router.get("", response_model=ChallengeListResponse)
def list_challenges() -> ChallengeListResponse:
    challenges = challenge_service.list_challenges()
    return ChallengeListResponse(challenges=challenges)


@router.get("/{challenge_id}", response_model=ChallengeDetail)
def challenge_detail(challenge_id: str) -> ChallengeDetail:
    try:
        return challenge_service.get_challenge(challenge_id)
    except KeyError as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=404, detail=str(exc)) from exc
