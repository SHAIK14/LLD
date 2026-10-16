def run_once(self):
    now = time.time()
    for job in self.scheduler.store.running_jobs():   # only RUNNING jobs
        if now > job.lease_until:                     # lease ran out
            self.scheduler.requeue(job)               # back to PENDING + heap
