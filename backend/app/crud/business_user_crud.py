import asyncpg

async def get_loyalty_program_id_by_business_user_id(pool: asyncpg.Pool, business_user_id: int) -> int:
    query = "SELECT loyalty_program_id FROM business_user WHERE id = $1;"
    async with pool.acquire() as conn:
        result = await conn.fetchrow(query, business_user_id)
        if result:
            return result["loyalty_program_id"]
        return None
