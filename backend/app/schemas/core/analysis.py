from pydantic import BaseModel, Field
from typing import List

class AnalysisSummaryResponse(BaseModel):
    summary: str = Field(description="A concise, data-driven summary of the key findings from the analysis.")
    recommendations: List[str] = Field(description="A list of actionable recommendations based on the summary.")
