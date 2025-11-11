import asyncpg
import json
from typing import Dict, Any

class OfferCRUD:
    async def save_template_offers(
        self,
        pool: asyncpg.Pool,
        loyalty_program_id: int,
        template_id: str,
        offers_data: Dict[str, Any]
    ) -> int:
        """
        Save generated template offers to DB.
        Adjust table/columns to match your schema.
        """
        query = """
            INSERT INTO offer_suggestions (loyalty_program_id, template_id, offers_json, created_at)
            VALUES ($1, $2, $3, NOW())
            RETURNING id
        """
        async with pool.acquire() as conn:
            offer_id = await conn.fetchval(
                query,
                loyalty_program_id,
                template_id,
                json.dumps(offers_data)
            )
        return offer_id

offer_crud = OfferCRUD()