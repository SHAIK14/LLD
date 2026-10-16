from models.job_status import JobStatus

class JobStore:
    def __init__(self):
        self._jobs = {}    # job_id → Job
        self._keys = {}    # key → job_id
        self._dead = []    # dead jobs

    def add(self, job):
        self._jobs[job.job_id] = job
        if job.key is not None:
            self._keys[job.key] = job.job_id

    def get(self, job_id):
        return self._jobs.get(job_id)

    def find_by_key(self, key):
        return self._keys.get(key)

    def running_jobs(self):
        result = []
        for job in self._jobs.values():
            if job.status == JobStatus.RUNNING:
                result.append(job)
        return result

    def add_dead(self, job):
        self._dead.append(job)
