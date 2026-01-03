import json
import boto3
from typing import override
from domain.models.job_models import JobRequest
from domain.queue.queue_interface import QueueInterface
from domain.settings.settings import get_settings
from services.logger.logger import get_logger

logger = get_logger()
settings = get_settings()


class SQSQueue(QueueInterface):

    def __init__(self):
        self.sqs_client = boto3.client(
            "sqs",
            region_name=settings.aws_region
        )
        self.queue_url = settings.sqs_queue_url

    @override
    def enqueue(self, job: JobRequest) -> None:
        """
        Send a job to the SQS queue.
        :param job: dict containing job_id, operation, payload, callback_url, etc.
        """
        try:
            response = self.sqs_client.send_message(
                QueueUrl=self.queue_url,
                MessageBody=json.dumps(job.to_dict())
            )
            logger.info(
                "Job enqueued in SQS",
                job_id=job.job_id,
                message_id=response.get("MessageId")
            )
        except Exception as e:
            logger.error("Failed to enqueue job in SQS", error=str(e), job_id=job.job_id)
