import threading
import time
import uuid

from models.job import Job
from models.job_status import JobStatus

class Scheduler:
    def __init__(self, store, queue, retry_policy, lease_seconds=30):
        self.store = store
        self.queue = queue
        self.retry_policy = retry_policy
        self.lease_seconds = lease_seconds
        self.lock = threading.Lock()

    def submit(self, func, args, run_at, priority=0, key=None):
        with self.lock:
            if key is not None:
                old_id = self.store.find_by_key(key)
                if old_id is not None:
                    return old_id

            job_id = str(uuid.uuid4())
            job = Job(job_id, func, args, run_at, priority, key)
            self.store.add(job)
            self.queue.push(job)
            return job_id

    def cancel(self, job_id):
        with self.lock:
            job = self.store.get(job_id)
            if job is None or job.status != JobStatus.PENDING:
                return False
            job.status = JobStatus.CANCELLED
            return True

    def get_status(self, job_id):
        job = self.store.get(job_id)
        if job is None:
            return None
        return job.status

    def claim_next(self):
        with self.lock:
            job = self.queue.peek()
            if job is None:
                return None
            if job.run_at > time.time():
                return None

            self.queue.pop()
            if job.status != JobStatus.PENDING:
                return None

            job.status = JobStatus.RUNNING
            job.lease_until = time.time() + self.lease_seconds
            return job

    def report_success(self, job):
        job.status = JobStatus.SUCCEEDED

    def report_failure(self, job):
        job.attempts += 1
        if job.attempts < job.max_attempts:
            delay = self.retry_policy.next_delay(job.attempts)
            job.run_at = time.time() + delay
            self.requeue(job)
        else:
            job.status = JobStatus.DEAD
            self.store.add_dead(job)

    def requeue(self, job):
        with self.lock:
            job.status = JobStatus.PENDING
            self.queue.push(job)
