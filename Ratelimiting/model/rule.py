


class RateLimitRule:
    def __int__(self,max_request:int, window_seconds:int):
        self.max_request = max_request
        self.window_seconds = window_seconds
