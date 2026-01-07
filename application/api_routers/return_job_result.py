import json
from fastapi import APIRouter, Request, BackgroundTasks
from services.logger.logger import get_logger
from application.providers.datalake_provider import get_datalake_service
from application.api_routers.utils import update_records_with_results, return_result_to_callback_url
from domain.settings.settings import get_settings
from domain.models.job_models import JobResult

router = APIRouter()

logger = get_logger()


@router.post("/executed_operations")
async def return_job_result(request: Request, background_tasks: BackgroundTasks):
    settings = get_settings()

    if request.headers.get("Authorization") != f'Bearer {settings.auth_token}':
        return {"status": "unauthorized"}

    body = json.loads(await request.body())
    logger.info("Received job result", **body)

    background_tasks.add_task(update_records_with_results, JobResult(**body), get_datalake_service())
    background_tasks.add_task(return_result_to_callback_url, body.get('callback_url'), JobResult(**body))

    return {"status": "ok"}
