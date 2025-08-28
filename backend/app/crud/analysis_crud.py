import asyncpg
import json
from typing import List, Dict, Any, Optional
from app.utils.json_encoders import NumpyEncoder

class CRUDAnalysis:
    async def get_all_orders_as_list(self, pool: asyncpg.Pool, loyalty_program_id: int) -> List[Dict[str, Any]]:
        """Fetches all order JSON blobs for a given program."""
        query = "SELECT * FROM orders WHERE loyalty_program_id = $1;"
        
        async with pool.acquire() as conn:

            records = await conn.fetch(query, loyalty_program_id)
            
        if not records:
            return []

        return [json.loads(r['pos_raw_data']) for r in records if r['pos_raw_data']]

    async def save_analysis_result(
        self,
        pool: asyncpg.Pool,
        loyalty_program_id: int,
        analysis_type: int,
        result_dict: Dict[str, Any]
    ) -> int:
        """Saves a new analysis result to the database and returns its new ID."""
        query = """
            INSERT INTO analysis_results (loyalty_program_id, analysis_type, analysis_json, created_at, updated_at)
            VALUES ($1, $2, $3, NOW(), NOW())
            RETURNING id;
        """
        summary_json = json.dumps(result_dict, cls=NumpyEncoder)
        async with pool.acquire() as conn:
            new_id = await conn.fetchval(query, loyalty_program_id, analysis_type, summary_json)
        return new_id

    async def get_latest_analysis_result(
        self,
        pool: asyncpg.Pool,
        loyalty_program_id: int,
        analysis_type: int  # Now expects int
    ) -> Optional[Dict[str, Any]]:
        """Fetches the most recent analysis result for a given program and type."""
        query = """
            SELECT id, loyalty_program_id, analysis_type, analysis_json, created_at
            FROM analysis_results
            WHERE loyalty_program_id = $1 AND analysis_type = $2
            ORDER BY created_at DESC
            LIMIT 1;
        """
        async with pool.acquire() as conn:
            record = await conn.fetchrow(query, loyalty_program_id, analysis_type)
        return dict(record) if record else None

analysis_crud = CRUDAnalysis()