import uuid as uuid_pkg
from datetime import datetime, timezone
from typing import Dict, Any
from sqlmodel import Field, SQLModel
from app.models.enums import AnalysisType
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column

class AnalysisResult(SQLModel, table=True):
    __tablename__ = "analysis_results"
    id: uuid_pkg.UUID = Field(default_factory=uuid_pkg.uuid4, primary_key=True, index=True)
    analysis_type: AnalysisType
    analysis_json: Dict[str, Any] = Field(default_factory=dict,sa_column=Column(JSONB))
    loyalty_program_id: uuid_pkg.UUID = Field(foreign_key="loyalty_programs.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))