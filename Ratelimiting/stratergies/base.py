from abc import ABC ,abstractmethod
from models.rule import RateLimitRule

class RateLimitStrategy(ABC):

    @abstractmethod
    def allow(self, user_id:int, rule:RateLimitRule):
