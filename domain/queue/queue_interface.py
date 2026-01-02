from abc import ABC, abstractmethod
from domain.models.job import JobRequest


class QueueInterface(ABC):

    @abstractmethod
    def enqueue(self, job: JobRequest) -> None:
        """
        Send a job to the queue.
        """
        pass
