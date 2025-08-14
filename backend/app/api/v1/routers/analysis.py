import asyncpg
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, Query

from app.db.database import get_db_pool
from app.services import analysis_service
from app.crud.analysis_crud import analysis_crud
from app.api.deps import get_current_auth_data
from app.schemas import AuthData, AnalysisTypeEnum 
    
router = APIRouter()

@router.post("/run-all-analyses", status_code=202)
async def trigger_all_analyses(
    background_tasks: BackgroundTasks,
    pool: asyncpg.Pool = Depends(get_db_pool),
    auth_data: AuthData = Depends(get_current_auth_data)
):
    """
    Triggers all three analysis pipelines as a background job.
    The loyalty program ID is securely retrieved from the auth token.
    """
    background_tasks.add_task(
        analysis_service.trigger_all_analyses,
        pool,
        auth_data.loyalty_program_id
    )
    return {"message": "All analysis pipelines have been queued and are running in the background."}


@router.get("/results/latest")
async def get_latest_analysis(
    analysis_type: AnalysisTypeEnum,
    pool: asyncpg.Pool = Depends(get_db_pool),
    auth_data: AuthData = Depends(get_current_auth_data)
):
    """
    Retrieves the most recent analysis result for the user's loyalty program,
    filtered by the specified analysis type.
    """
    result = await analysis_crud.get_latest_analysis_result(
        pool=pool, 
        loyalty_program_id=auth_data.loyalty_program_id,
        analysis_type=analysis_type.value
    )
    
    if not result:
        raise HTTPException(
            status_code=404, 
            detail=f"No '{analysis_type.value}' analysis results found for this program."
        )
        
    return result