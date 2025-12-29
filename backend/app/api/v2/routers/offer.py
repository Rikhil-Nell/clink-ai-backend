import asyncpg
from fastapi import APIRouter, Depends, BackgroundTasks, Query
from app.db.database import get_db_pool
from app.api.deps import get_current_auth_data
from app.services import offer_service, forecast_service
from app.schemas.core import *
from app.schemas.core.enums import TemplateEnum

router = APIRouter()


@router.post("/generate-all-templates")
async def generate_all_templates(
    background_tasks: BackgroundTasks,
    pool: asyncpg.Pool = Depends(get_db_pool),
    auth_data: AuthData = Depends(get_current_auth_data)
):
    background_tasks.add_task(
        offer_service.generate_all_templates,
        pool,
        auth_data.loyalty_program_id
    )
    return {"message": f"Offer Generation has commenced for loyalty_id = {auth_data.loyalty_program_id}"}


@router.post("/update-template")
async def generate_one_template(
    background_tasks: BackgroundTasks,
    template_id: TemplateEnum = Query(..., description="Template ID"),
    pool: asyncpg.Pool = Depends(get_db_pool),
    auth_data: AuthData = Depends(get_current_auth_data)
):
    background_tasks.add_task(
        offer_service.generate_one_template,
        template_id.template_name,  # Converts int -> internal string name
        pool,
        auth_data.loyalty_program_id
    )
    return {"message": f"Offer Generation has commenced with template_id = {template_id.value}"}


@router.post("/generate-forecast")
async def generate_forecast(
    background_tasks: BackgroundTasks,
    template_id: TemplateEnum = Query(..., description="Template ID"),
    pool: asyncpg.Pool = Depends(get_db_pool),
    auth_data: AuthData = Depends(get_current_auth_data)
):
    background_tasks.add_task(
        forecast_service.generate_forecast,
        pool,
        auth_data.loyalty_program_id,
        template_id.template_name  # Converts int -> internal string name
    )
    
    return {"message": f"Forecast generation started for template_id = {template_id.value}"}
