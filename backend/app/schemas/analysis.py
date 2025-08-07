# app/schemas/analysis.py
from sqlmodel import SQLModel
from typing import Dict, Any
from datetime import datetime
from app.models.enums import AnalysisType

class AnalysisResultCreate(SQLModel):
    # The API will receive business_user_id, not loyalty_program_id
    business_user_id: int
    analysis_type: AnalysisType
    analysis_json: Dict[str, Any]

class AnalysisResultResponse(SQLModel):
    id: int
    business_user_id: int
    analysis_type: AnalysisType
    analysis_json: Dict[str, Any]
    created_at: datetime
    updated_at: datetime