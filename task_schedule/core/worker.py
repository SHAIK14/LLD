
class Worker:
    def __init__(self,scheduler):
        self.scheduler = scheduler

    def run_once(self):
        job = self.scheduler.claim_next()       # ask for a due job
        if job is None:
            return False                        # nothing to do right now

        try:
            job.run()                           # send_email("a@b.com", "Hi")
            self.scheduler.report_success(job)
        except Exception as error:
            print("   failed:", error)
            self.scheduler.report_failure(job)  # retry or dead
        return True
