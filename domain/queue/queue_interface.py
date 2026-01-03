from abc import ABC, abstractmethod
from domain.models.job_models import JobRequest


class QueueInterface(ABC):

    @abstractmethod
    def enqueue(self, job: JobRequest) -> None:
        """
        Send a job to the queue.
        """
        pass
