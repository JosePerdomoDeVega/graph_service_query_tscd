import json
import httpx
from services.logger.logger import get_logger
from domain.settings.settings import get_settings
from domain.datalake.datalake_interface import DataLakeInterface
from domain.models.job_models import JobResult

logger = get_logger()
settings = get_settings()


async def update_records_with_results(job_result: JobResult, datalake_manager: DataLakeInterface):
    with logger.span("Updating job result on datalake"):
        record = await datalake_manager.get_record(job_result.storage_key)
        logger.info(f"Previous record pulled from datalake", **job_result.to_dict())
        record.data['result'] = job_result.result
        record.data['errors'] = job_result.errors
        await datalake_manager.add_record(record)



async def return_result_to_callback_url(callback_url: str, result: JobResult):
    async with httpx.AsyncClient() as client:
        r = await client.post(callback_url, data=json.dumps(result.to_dict()), timeout=httpx.Timeout(30.0))
        if r.status_code != 200:
            raise Exception(f'HTTP status code {r.status_code}: {r.text}')
        else:
            return 200
