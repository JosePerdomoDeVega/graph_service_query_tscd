import json
import aioboto3
from typing import override
from domain.models.job_models import JobRequest
from domain.queue.queue_interface import QueueInterface
from domain.settings.settings import get_settings
from services.logger.logger import get_logger

logger = get_logger()
settings = get_settings()


class SQSQueue(QueueInterface):

    def __init__(self):
        self.session = None
        self.region = settings.aws_region
        self.queue_url = settings.sqs_queue_url

    async def create_session(self):
        self.session = aioboto3.Session(region_name=self.region).client('sqs')
        return self.session

    @override
    async def enqueue(self, job: JobRequest) -> None:
        """
        Send a job to the SQS queue.
        :param job: dict containing job_id, operation, payload, callback_url, etc.
        """
        try:
            async with await self.create_session() as sqs:
                response = await sqs.send_message(
                    QueueUrl=self.queue_url,
                    MessageBody=json.dumps(job.to_dict()))

            logger.info("Job enqueued in SQS", job_id=job.job_id, message_id=response.get("MessageId"))

        except Exception as e:
            logger.error("Failed to enqueue job in SQS", error=str(e), job_id=job.job_id)


