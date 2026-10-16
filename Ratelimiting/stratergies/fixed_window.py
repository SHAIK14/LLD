from model.rule import RateLimitRule
from stratergies.base import RateLimitStrategy

import time

class FixedWindowStrategy(RateLimitStrategy):
    def __init__(self):
        self._counts = {}          # user_id → how many requests in this window
        self._window_starts = {}   # user_id → when this window started

    def allow(self, user_id, rule):
        now = time.monotonic()

        # first time we see this user → start their window now
        if user_id not in self._counts:
            self._counts[user_id] = 0
            self._window_starts[user_id] = now

        # window is over → reset
        if now - self._window_starts[user_id] >= rule.window_seconds:
            self._counts[user_id] = 0
            self._window_starts[user_id] = now

        # room left → allow
        if self._counts[user_id] < rule.max_requests:
            self._counts[user_id] += 1
            return True

        return False
