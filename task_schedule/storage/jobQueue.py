import heapq

class JobQueue:
    def __init__(self):
        self._heap =[]

    def push (self,job):
        heapq.heappush(self._heap ,(job.run_at, -job.priority, job.job_id, job))


    def peek(self):
        if not self._heap:
            return None
        return self._heap[0][3]

    def pop(self):
        if not self._heap:
            return None

        return heapq.heappop(self._heap)[3]
