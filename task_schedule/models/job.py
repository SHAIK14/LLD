from models.job_status import JobStatus
class Job:
    def __init__(self, job_id, func, args, run_at, priority=0, key=None, max_attempts=3):
        self.job_id = job_id
        self.func = func
        self.args = args
        self.run_at = run_at
        self.priority = priority
        self.key = key
        self.status = JobStatus.PENDING
        self.attempts = 0
        self.max_attempts = max_attempts
        self.lease_until = None

    def run(self):
        return self.func(*self.args)
