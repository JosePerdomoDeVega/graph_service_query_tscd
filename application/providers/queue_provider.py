from domain.settings.settings import get_settings
from services.queue.sqs_queue import SQSQueue


def get_queue_service():
    settings = get_settings()

    if settings.queue_implementation == 'AWS_SQS':
        return SQSQueue()

    return None
