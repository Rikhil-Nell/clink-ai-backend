import asyncpg
import pandas as pd
from typing import List, Dict, Any, Optional

class CRUDAnalysis:
    async def get_all_orders_as_df(self, pool: asyncpg.Pool, loyalty_program_id: int) -> pd.DataFrame:
        """Fetches all orders for a given program and returns them as a Pandas DataFrame."""
    
        query = "SELECT * FROM orders WHERE loyalty_program_id = $1;"
        
        async with pool.acquire() as conn:
            records = await conn.fetch(query, loyalty_program_id)
            
        if not records:
            return pd.DataFrame()
            
        return pd.DataFrame([dict(r) for r in records])

    async def save_analysis_result(
        self, 
        pool: asyncpg.Pool, 
        loyalty_program_id: int, 
        analysis_type: str, 
        result_json: Dict[str, Any]
    ) -> int:
        """Saves a new analysis result to the database and returns its new ID."""
        query = """
            INSERT INTO analysis_results (loyalty_program_id, analysis_type, analysis_json, created_at, updated_at)
            VALUES ($1, $2, $3, NOW(), NOW())
            RETURNING id;
        """
        async with pool.acquire() as conn:
            new_id = await conn.fetchval(query, loyalty_program_id, analysis_type, result_json)
        return new_id

    async def get_latest_analysis_result(
        self, 
        pool: asyncpg.Pool, 
        loyalty_program_id: int,
        analysis_type: str
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