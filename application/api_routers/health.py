from fastapi import APIRouter, status
from services.queue.sqs_queue import SQSQueue
from services.datalake.s3_datalake import S3DataLake
from services.logger.logger import get_logger

router = APIRouter()
logger = get_logger()


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint.
    Returns status of API, SQS queue, and DataLake.
    """
    status_report = {
        "api": "ok",
        "sqs": None,
        "datalake": None
    }

    try:
        sqs = SQSQueue()
        sqs.sqs_client.get_queue_attributes(
            QueueUrl=sqs.queue_url,
            AttributeNames=["QueueArn"]
        )
        status_report["sqs"] = "ok"

    except Exception as e:
        logger.error("SQS health check failed", error=str(e))
        status_report["sqs"] = f"error: {str(e)}"

    try:
        datalake = S3DataLake()
        _ = datalake.get_prefix()
        status_report["datalake"] = "ok"

    except Exception as e:
        logger.error("DataLake health check failed", error=str(e))
        status_report["datalake"] = f"error: {str(e)}"

    return status_report
