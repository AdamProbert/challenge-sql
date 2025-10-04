from __future__ import annotations

import os
from functools import lru_cache
from typing import Dict, List

from slugify import slugify

from pokedex import challenge_loader
from ..schemas import ChallengeDetail, ChallengeSchemaColumn, ChallengeSchemaTable, ChallengeSummary


def _challenge_id(challenge: dict) -> str:
    # e.g. beginner/01 -> beginner-01-title-slug
    rel_path = os.path.relpath(challenge.get("dir", ""), "challenges")
    rel_path = rel_path.replace("\\", "/")
    directory_part = rel_path

    # Append slugified title to avoid duplicates between difficulties
    title_slug = slugify(challenge.get("title", "challenge"))
    return f"{directory_part}:{title_slug}"


def _challenge_order(challenge: dict) -> int:
    try:
        dirname = os.path.basename(challenge.get("dir", ""))
        return int(dirname)
    except (TypeError, ValueError):
        return 0


@lru_cache
def _load_catalog() -> List[dict]:
    return challenge_loader.load_challenges()


def list_challenges() -> Dict[str, List[ChallengeSummary]]:
    challenges_by_difficulty: Dict[str, List[ChallengeSummary]] = {}

    for challenge in _load_catalog():
        difficulty = (challenge.get("difficulty") or "unknown").lower()
        summary = ChallengeSummary(
            id=_challenge_id(challenge),
            title=challenge.get("title", "Untitled Challenge"),
            difficulty=difficulty,
            order=_challenge_order(challenge),
        )
        challenges_by_difficulty.setdefault(difficulty, []).append(summary)

    for summaries in challenges_by_difficulty.values():
        summaries.sort(key=lambda s: s.order)

    return challenges_by_difficulty


def get_challenge(challenge_id: str) -> ChallengeDetail:
    for challenge in _load_catalog():
        if _challenge_id(challenge) == challenge_id:
            details = challenge.get("challenge", {})
            return ChallengeDetail(
                id=challenge_id,
                title=challenge.get("title", "Untitled Challenge"),
                description=challenge.get("description", ""),
                difficulty=(challenge.get("difficulty") or "unknown").lower(),
                task=details.get("task", ""),
                hints=details.get("hints", []) or [],
                expected_columns=details.get("expected_columns", []) or [],
            )
    raise KeyError(f"Challenge not found: {challenge_id}")


def resolve_challenge_path(challenge_id: str) -> str:
    for challenge in _load_catalog():
        if _challenge_id(challenge) == challenge_id:
            return challenge.get("dir")
    raise KeyError(f"Challenge not found: {challenge_id}")
