import json
from fastapi import APIRouter, HTTPException
import uuid
from application.providers.datalake_provider import get_datalake_service
from application.providers.queue_provider import get_queue_service
from services.logger.logger import get_logger
from domain.models.job import JobRequest, JobResponse

logger = get_logger()
router = APIRouter()


def enqueue_job(job_request: JobRequest) -> str:
    job_request.job_id = str(uuid.uuid4())

    queue_service = get_queue_service()
    queue_service.enqueue(job_request)

    datalake_service = get_datalake_service()
    datalake_service.add_record({
        "job_id": job_request.job_id,
        "timestamp": datalake_service.get_prefix(),
        "payload": json.dumps(job_request.to_dict()),
    })

    logger.info("Job enqueued", job_id=job_request.job_id, operation=job_request.operation)
    return job_request.job_id


@router.post("/jobs", response_model=JobResponse)
async def submit_job(request: JobRequest):
    """
    Submit a graph operation job to the queue.
    """
    try:
        job_id = enqueue_job(request)
        return JobResponse(job_id=job_id)
    except Exception as e:
        logger.error("Failed to enqueue job", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
