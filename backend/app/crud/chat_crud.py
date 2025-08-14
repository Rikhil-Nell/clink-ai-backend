import asyncpg
from typing import List, Dict, Any

class CRUDChat:
    async def fetch_chat_history(
        self, 
        pool: asyncpg.Pool, 
        loyalty_program_id: int, 
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Fetches the most recent chat messages for a program, up to a specified limit.
        """
        query = """
            SELECT role, content, bot_response_type created_at 
            FROM chat_messages 
            WHERE loyalty_program_id = $1 
            ORDER BY created_at DESC 
            LIMIT $2;
        """
        async with pool.acquire() as conn:
            records = await conn.fetch(query, loyalty_program_id, limit)
        
        # The records are fetched in reverse chronological order (newest first).
        # We reverse the list so it's in chronological order for the frontend.
        messsages = [dict(r) for r in reversed(records)]

        return messsages 
    
    async def insert_chat_message(self, pool: asyncpg.Pool, loyalty_program_id: int, role: str, content: str):
        """Inserts a single chat message into the database."""
        query = "INSERT INTO chat_messages (loyalty_program_id, role, content, created_at) VALUES ($1, $2, $3, NOW());"
        async with pool.acquire() as conn:
            await conn.execute(query, loyalty_program_id, role, content)

chat_crud = CRUDChat()