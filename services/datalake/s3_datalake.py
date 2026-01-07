import json
import aioboto3
import datetime
from typing import override
from domain.datalake.datalake_interface import DataLakeInterface
from domain.models.record_models import DataLakeRecord
from domain.settings.settings import get_settings

settings = get_settings()


class S3DataLake(DataLakeInterface):

    def __init__(self):
        self.session = None
        self.bucket_name = settings.aws_bucket_name
        self.region = settings.aws_region

    async def create_session(self):
        self.session = aioboto3.Session(region_name=self.region).client('s3')
        return self.session

    @override
    async def add_record(self, record: DataLakeRecord) -> str:
        """
        Persist a record in S3 using a date-based prefix.
        """
        prefix = self.get_prefix()
        key = f"{prefix}/{record.record_id}.json"

        async with await self.create_session() as s3:
            await s3.put_object(Bucket=self.bucket_name, Key=key,
                                Body=json.dumps(record.data), ContentType="application/json")

        return key

    @override
    async def get_record(self, key: str) -> DataLakeRecord:
        async with await self.create_session() as s3:
            response = await s3.get_object(Bucket=self.bucket_name, Key=key)

            async with response["Body"] as stream:
                body = await stream.read()

        record = json.loads(body.decode())

        return DataLakeRecord(record_id=record.get("job_id"), data=record)


    @override
    def get_prefix(self) -> str:
        """
        Return a date-based prefix for record storage.
        """
        return datetime.datetime.utcnow().strftime("%Y/%m/%d/%H")
