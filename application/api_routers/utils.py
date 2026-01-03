from services.logger.logger import get_logger
from domain.datalake.datalake_interface import DataLakeInterface
from domain.models.job_models import JobResult

logger = get_logger()


def update_records_with_results(job_result: JobResult, datalake_manager: DataLakeInterface):
    with logger.span("Updating job result on datalake"):
        record = datalake_manager.get_record(job_result.storage_key)
        logger.info(f"Previous record pulled from datalake", **job_result.to_dict())
        record.data['result'] = job_result.result
        record.data['errors'] = job_result.errors
        datalake_manager.add_record(record)
