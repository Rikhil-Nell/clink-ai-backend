import asyncpg
import json
from typing import Dict, Any, List, Optional
from app.schemas.core.enums import GoalEnum

class OfferCRUD:
    async def save_template_offers(
        self,
        pool: asyncpg.Pool,
        loyalty_program_id: int,
        template_id: int,
        goal_ids: List[int],
        generation_uuid: str,
        offers_data: Dict[str, Any],
        forecast_data: Dict[str, Any]
    ) -> List[int]:
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
                (goal_name, template_id, order_id, loyalty_program_id, pos_raw_data, ai_forecast_response, created_at, updated_at)
            VALUES 
                ($1, $2, $3, $4, $5, $6, NOW(), NOW())
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
                    generation_uuid,
                    loyalty_program_id,
                    json.dumps(offers_data),
                    json.dumps(forecast_data)
                )
                inserted_ids.append(offer_id)
        
        return inserted_ids
    
    async def get_latest_offer(
        self,
        pool: asyncpg.Pool,
        loyalty_program_id: int,
        template_id: int
    ) -> Optional[Dict[str, Any]]:
        """Fetches the most recent offer for a given program and template."""
        query = """
            SELECT 
                id, 
                goal_name, 
                template_id, 
                loyalty_program_id, 
                pos_raw_data, 
                ai_forecast_response, 
                created_at
            FROM ai_suggestions
            WHERE loyalty_program_id = $1 AND template_id = $2
            ORDER BY created_at DESC
            LIMIT 1
        """
        async with pool.acquire() as conn:
            record = await conn.fetchrow(query, loyalty_program_id, template_id)
        return dict(record) if record else None

    async def update_ai_forecast_response(
        self,
        pool: asyncpg.Pool,
        offer_id: int,
        forecast_data: Dict[str, Any]
    ) -> bool:
        """
        Update the ai_forecast_response field for a specific offer.
        
        Args:
            pool: Database connection pool
            offer_id: ID of the offer to update
            forecast_data: Forecast data to store
            
        Returns:
            True if update succeeded, False otherwise
        """
        query = """
            UPDATE ai_suggestions
            SET 
                ai_forecast_response = $1,
                updated_at = NOW()
            WHERE id = $2
            RETURNING id
        """
        
        async with pool.acquire() as conn:
            result = await conn.fetchval(
                query,
                json.dumps(forecast_data),
                offer_id
            )
        
        return result is not None
    
    async def update_forecast_for_template(
        self,
        pool: asyncpg.Pool,
        loyalty_program_id: int,
        template_id: int,
        forecast_data: Dict[str, Any]
    ) -> int:
        """
        Update ai_forecast_response for the LATEST offer of a specific template.
        Only updates the most recent row (highest id) for the given template.
        
        Returns:
            Number of rows updated (0 or 1)
        """
        query = """
            UPDATE ai_suggestions
            SET 
                ai_forecast_response = $1,
                updated_at = NOW()
            WHERE id = (
                SELECT id FROM ai_suggestions
                WHERE loyalty_program_id = $2 
                  AND template_id = $3
                ORDER BY id DESC
                LIMIT 1
            )
            RETURNING id
        """
        
        async with pool.acquire() as conn:
            result = await conn.fetchval(
                query,
                json.dumps(forecast_data),
                loyalty_program_id,
                template_id
            )
        
        return 1 if result is not None else 0

offer_crud = OfferCRUD()