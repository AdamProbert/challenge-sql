from __future__ import annotations

from collections import deque
from threading import Lock
from time import monotonic
from typing import Deque, Dict

from ..config import get_settings


class RateLimitExceeded(Exception):
    """Raised when a session exceeds the allowed request rate."""


class InMemoryRateLimiter:
    def __init__(self) -> None:
        settings = get_settings()
        self.limit = settings.rate_limit_requests
        self.window = settings.rate_limit_window_seconds
        self._events: Dict[str, Deque[float]] = {}
        self._lock = Lock()

    def check(self, key: str) -> None:
        now = monotonic()
        with self._lock:
            bucket = self._events.setdefault(key, deque())

            while bucket and now - bucket[0] > self.window:
                bucket.popleft()

            if len(bucket) >= self.limit:
                raise RateLimitExceeded(
                    f"Rate limit exceeded: {self.limit} requests within {self.window} seconds"
                )

            bucket.append(now)


_rate_limiter = InMemoryRateLimiter()


def enforce_rate_limit(key: str) -> None:
    _rate_limiter.check(key)
