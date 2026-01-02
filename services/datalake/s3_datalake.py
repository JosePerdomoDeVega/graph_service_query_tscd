import json
import datetime
import boto3
from typing import override
from domain.datalake.datalake_interface import DataLakeInterface
from domain.models.record import DataLakeRecord
from domain.settings.settings import get_settings
from services.logger.logger import get_logger

settings = get_settings()
logger = get_logger()


class S3DataLake(DataLakeInterface):

    def __init__(self):

        self.bucket_name = settings.aws_bucket_name
        self.s3_client = boto3.client("s3", region_name=settings.aws_region)

        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self) -> None:
        """
        Ensure the S3 bucket exists. If not, create it.
        """
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)

        except Exception as e:

            logger.info("Datalake bucket does not exist. Creating bucket.", bucket=self.bucket_name)

            self.s3_client.create_bucket(
                Bucket=self.bucket_name,
                CreateBucketConfiguration={
                    "LocationConstraint": settings.aws_region
                }
            )

    @override
    def add_record(self, record: DataLakeRecord) -> None:
        """
        Persist a record in S3 using a date-based prefix.
        """
        prefix = self.get_prefix()
        key = f"{prefix}/{record.record_id}.json"

        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=key,
            Body=json.dumps(record.data),
            ContentType="application/json"
        )

        logger.info("Record stored in datalake", bucket=self.bucket_name, key=key, record_id=record.record_id)

    @override
    def get_prefix(self) -> str:
        """
        Return a date-based prefix for record storage.
        """
        return datetime.datetime.utcnow().strftime("%Y/%m/%d/%H")
