from pydantic import BaseModel, HttpUrl, model_validator
from typing import Any, Dict, Optional, List


class Job(BaseModel):
    job_id: str
    operation: str
    payload: Dict[str, Any]
    callback_url: str

    def to_dict(self) -> Dict[str, Any]:
        return dict(
            job_id=self.job_id,
            operation=self.operation,
            payload=self.payload,
            callback_url=self.callback_url,
        )


class JobRequest(BaseModel):
    job_id: Optional[str] = None
    operation: str
    start_word: Optional[str] = None
    end_word: Optional[str] = None
    max_depth: Optional[int] = 10
    degree: Optional[int] = None
    callback_url: HttpUrl

    @model_validator(mode="after")
    def check_operation_and_params(cls, model):
        """
        Validate that the operation is allowed and required parameters are present.
        """
        op = model.operation
        if op not in VALID_OPERATIONS:
            raise ValueError(f"Invalid operation: {op}. Must be one of {VALID_OPERATIONS}")

        if op in ["min_path", "all_paths", "max_distance"]:
            if not model.start_word or not model.end_word:
                raise ValueError(f"Operation '{op}' requires 'start_word' and 'end_word'")

        if op == "nodes_by_connectivity" and model.degree is None:
            raise ValueError(f"Operation '{op}' requires 'degree'")

        return model

    def to_dict(self) -> Dict[str, Any]:
        return dict(
            job_id=self.job_id,
            operation=self.operation,
            start_word=self.start_word,
            end_word=self.end_word,
            max_depth=str(self.max_depth),
            degree=str(self.degree),
            callback_url=str(self.callback_url)
        )


class JobResponse(BaseModel):
    job_id: str
    status: str = "queued"


VALID_OPERATIONS: List[str] = [
    "min_path",
    "all_paths",
    "max_distance",
    "cluster_identification",
    "high_connectivity_nodes",
    "nodes_by_connectivity",
    "isolated_nodes"
]
