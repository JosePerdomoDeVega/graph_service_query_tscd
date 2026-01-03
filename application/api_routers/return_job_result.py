import json
from fastapi import APIRouter, Request
from services.logger.logger import get_logger
from application.providers.datalake_provider import get_datalake_service
from application.api_routers.utils import update_records_with_results
from domain.settings.settings import get_settings
from domain.models.job_models import JobResult

router = APIRouter()

logger = get_logger()


@router.post("/executed_operations")
async def return_job_result(request: Request):
    settings = get_settings()
    if request.headers.get("Authorization") == f'Bearer {settings.auth_token}':
        body = json.loads(await request.body())
        logger.info('Received job result and has correct format', **body)
        update_records_with_results(JobResult(**body), get_datalake_service())


    return {"status": "ok"}
