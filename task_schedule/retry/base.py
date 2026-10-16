from abc import ABC, abstractmethod

class RetryPolicy(ABC):
    @abstractmethod
    def next_delay(self,attempt):
        ...
