from fastapi import APIRouter, HTTPException, BackgroundTasks
import uuid
from application.providers.datalake_provider import get_datalake_service
from application.providers.queue_provider import get_queue_service
from domain.models.record_models import DataLakeRecord
from services.logger.logger import get_logger
from domain.models.job_models import JobRequest

logger = get_logger()
router = APIRouter()


@router.post("/jobs")
async def submit_job(request: JobRequest, background_tasks: BackgroundTasks):
    """
    Submit a graph operation job to the queue.
    """
    try:
        background_tasks.add_task(enqueue_job, request)
        return {"status": "ok"}
    except Exception as e:
        logger.error("Failed to enqueue job", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
        return {"status": "error"}


async def enqueue_job(job_request: JobRequest) -> str:
    job_request.job_id = str(uuid.uuid4())

    datalake_service = get_datalake_service()
    key = await datalake_service.add_record(DataLakeRecord(record_id=job_request.job_id, data=job_request.to_dict()))
    job_request.storage_key = key

    queue_service = get_queue_service()
    await queue_service.enqueue(job_request)

    return job_request.job_id
