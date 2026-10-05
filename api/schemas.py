from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    algorithm_id: str
    size: int = 10
    preset_name: Optional[str] = None
    input_type: Optional[str] = "random"


class RunRequest(BaseModel):
    algorithm_id: str
    input: Dict[str, Any]


class CompareRequest(BaseModel):
    group: str
    algorithm_ids: List[str]
    input_kind: str
    sizes: List[int] = Field(default_factory=lambda: [10, 50, 100, 500, 1000])
    repeats: int = 3
    seed: int = 42


class APIErrorPayload(BaseModel):
    code: str
    message: str
    field: Optional[str] = None


class APIErrorResponse(BaseModel):
    error: APIErrorPayload
