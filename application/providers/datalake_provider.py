from domain.settings.settings import get_settings
from services.datalake.s3_datalake import S3DataLake


def get_datalake_service():
    settings = get_settings()

    if settings.datalake_implementation == 'AWS_S3':
        return S3DataLake()

    return None
