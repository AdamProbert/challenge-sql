from __future__ import annotations

from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class ChallengeSummary(BaseModel):
    id: str
    title: str
    difficulty: str
    order: int = Field(description="Challenge ordering within its difficulty group")


class ChallengeSchemaColumn(BaseModel):
    name: str
    data_type: str


class ChallengeSchemaTable(BaseModel):
    table_name: str
    columns: List[ChallengeSchemaColumn]


class ChallengeDetail(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: str
    title: str
    description: str
    difficulty: str
    task: str
    hints: List[str]
    expected_columns: List[str]
    schema_: List[ChallengeSchemaTable] = Field(default_factory=list, alias="schema")

    @property
    def schema(self) -> List[ChallengeSchemaTable]:  # pragma: no cover - accessor for convenience
        return self.schema_


class ChallengeListResponse(BaseModel):
    challenges: Dict[str, List[ChallengeSummary]]


class SessionCreateResponse(BaseModel):
    session_id: UUID


class SessionResetRequest(BaseModel):
    challenge_id: str


class QueryRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    sql: str
    challenge_id: Optional[str] = None
    validate_result: bool = Field(default=False, alias="validate")


class QueryResult(BaseModel):
    columns: List[str]
    rows: List[List[Optional[str]]]
    row_count: int
    execution_time_ms: float


class ValidationDetail(BaseModel):
    success: bool
    message: str


class QueryResponse(BaseModel):
    result: Optional[QueryResult]
    validation: Optional[ValidationDetail]


class ErrorResponse(BaseModel):
    detail: str
