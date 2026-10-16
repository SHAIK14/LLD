from retry.base import RetryPolicy


class FixedRetry(RetryPolicy):
    def __init__(self, delay=5):
        self.delay = delay

    def next_delay(self, attempt):
        return self.delay
