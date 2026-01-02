from pydantic import BaseModel
from typing import Any, Dict


class DataLakeRecord(BaseModel):
    record_id: str
    data: Dict[str, Any]
