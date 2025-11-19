import asyncpg
import json
from typing import Dict, Any, List
from app.schemas.core.enums import GoalEnum

class OfferCRUD:
    async def save_template_offers(
        self,
        pool: asyncpg.Pool,
        loyalty_program_id: int,
        template_id: int,
        goal_ids: List[int],
        offers_data: Dict[str, Any],
        forecast_data: Dict[str, Any]
    ) -> int:
        """
        Save generated template offers to DB.
        Creates one row per goal that the template maps to.
        """
        # Map goal_id to goal_name
        goal_names = {
            GoalEnum.INCREASE_AOV.value: "Increase AOV",
            GoalEnum.REPEAT_CUSTOMERS.value: "Repeat Customers",
            GoalEnum.INCREASE_OCCUPANCY.value: "Increase Occupancy Rate"
        }
        
        query = """
            INSERT INTO ai_suggestions 
                (goal_name, template_id, loyalty_program_id, pos_raw_data, ai_forecast_response, created_at, updated_at)
            VALUES 
                ($1, $2, $3, $4, $5, NOW(), NOW())
            RETURNING id
        """
        
        inserted_ids = []
        async with pool.acquire() as conn:
            # Insert one row per goal
            for goal_id in goal_ids:
                goal_name = goal_names.get(goal_id, "Unknown Goal")
                offer_id = await conn.fetchval(
                    query,
                    goal_name,
                    template_id,
                    loyalty_program_id,
                    json.dumps(offers_data),
                    json.dumps(forecast_data)
                )
                inserted_ids.append(offer_id)
        
        return inserted_ids  # Return all inserted IDs

offer_crud = OfferCRUD()