from fastapi import APIRouter, HTTPException
import uuid
from application.providers.datalake_provider import get_datalake_service
from application.providers.queue_provider import get_queue_service
from domain.models.record_models import DataLakeRecord
from services.logger.logger import get_logger
from domain.models.job_models import JobRequest

logger = get_logger()
router = APIRouter()


def enqueue_job(job_request: JobRequest) -> str:
    job_request.job_id = str(uuid.uuid4())

    datalake_service = get_datalake_service()
    key = datalake_service.add_record(DataLakeRecord(record_id=job_request.job_id, data=job_request.to_dict()))
    job_request.storage_key = key

    queue_service = get_queue_service()
    queue_service.enqueue(job_request)

    return job_request.job_id


@router.post("/jobs")
async def submit_job(request: JobRequest):
    """
    Submit a graph operation job to the queue.
    """
    try:
        job_id = enqueue_job(request)
        return {"status": "ok"}
    except Exception as e:
        logger.error("Failed to enqueue job", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
