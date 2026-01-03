from pydantic import BaseModel
from typing import Any, Dict

# Todo Añadir atributo del resultado
class DataLakeRecord(BaseModel):
    record_id: str
    data: Dict[str, Any]
