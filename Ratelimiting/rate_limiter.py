class RateLimiter:
    _instance = None          # the ONE shared object lives here

    def __init__(self, strategy, rules):
        self._strategy = strategy     # FixedWindow or TokenBucket
        self._rules = rules           # {Tier.FREE: rule, Tier.PREMIUM: rule}

    @classmethod
    def get_instance(cls, strategy=None, rules=None):
        if cls._instance is None:
            cls._instance = cls(strategy, rules)
        return cls._instance

    def set_strategy(self, strategy):
        self._strategy = strategy

    def allow_request(self, user):
        rule = self._rules[user.tier]
        return self._strategy.allow(user.user_id, rule)
