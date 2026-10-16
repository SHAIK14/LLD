from model.rule import RateLimitRule
from stratergies.base import RateLimitStrategy
class TokenBucketStrategy(RateLimitStrategy):
    def __init__(self):
        self._tokens = {}         # user_id → how many tokens left
        self._last_refill = {}    # user_id → when we last added tokens

    def allow(self, user_id, rule):
        now = time.monotonic()
        capacity = rule.max_requests                            # bucket size: 10
        refill_rate = rule.max_requests / rule.window_seconds   # 10 / 60 = 0.167 tokens per second

        # first time we see this user → give a full bucket
        if user_id not in self._tokens:
            self._tokens[user_id] = capacity
            self._last_refill[user_id] = now

        # add tokens for the time that passed
        seconds_passed = now - self._last_refill[user_id]
        new_tokens = seconds_passed * refill_rate
        self._tokens[user_id] = min(capacity, self._tokens[user_id] + new_tokens)
        self._last_refill[user_id] = now

        # have a token → spend it, allow
        if self._tokens[user_id] >= 1:
            self._tokens[user_id] -= 1
            return True

        return False
