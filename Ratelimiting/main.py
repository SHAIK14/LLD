from model.tier import Tier
from model.user import User
from model.rule import RateLimitRule
from rate_limiter import RateLimiter
from stratergies.fixed_window import FixedWindowStrategy
from stratergies.token_bucket import TokenBucketStrategy

rules = {
    Tier.FREE: RateLimitRule(10, 60),
    Tier.PREMIUM: RateLimitRule(100, 60),
}

alice = User("alice", Tier.FREE)
bob = User("bob", Tier.PREMIUM)

limiter = RateLimiter.get_instance(FixedWindowStrategy(), rules)

# alice sends 12 requests
for i in range(12):
    print("alice request", i + 1, limiter.allow_request(alice))

# bob sends 12 requests
for i in range(12):
    print("bob request", i + 1, limiter.allow_request(bob))

# singleton check
print("same limiter?", limiter is RateLimiter.get_instance())
