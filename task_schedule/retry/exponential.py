from retry.base import RetryPolicy

class ExponentialRetry(RetryPolicy):
    def __init__(self, base=2):
        self.base = base

    def next_delay(self, attempt):
        return self.base * (2 ** (attempt - 1))
