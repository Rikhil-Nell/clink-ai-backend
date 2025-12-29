import asyncpg
from typing import Optional

from app.schemas.core.logo import LogoInfo

class CRUDLogo:
    async def get_logo_key_for_loyalty_program(
        self,
        pool: asyncpg.Pool, 
        loyalty_program_id: int
    ) -> Optional[LogoInfo]:
        """
        Fetch the S3 key for a loyalty program's logo from ActiveStorage tables.
        
        This queries the Rails ActiveStorage tables to find the blob key
        that corresponds to the logo attachment for a given loyalty program.
        
        Args:
            db: Database session
            loyalty_program_id: The ID of the loyalty program
            
        Returns:
            LogoInfo with S3 key, filename, and content_type, or None if not found
        """
        query = """
            SELECT b.key, b.filename, b.content_type
            FROM active_storage_attachments a
            JOIN active_storage_blobs b ON b.id = a.blob_id
            WHERE a.record_type = 'LoyaltyProgram'
            AND a.name = 'logo'
            AND a.record_id = $1
        """
        async with pool.acquire() as conn:
            row = await conn.fetchrow(query, loyalty_program_id)
        
        if row:
            return LogoInfo(
                key=row['key'],
                filename=row['filename'],
                content_type=row['content_type']
            )
        return None
    
logo_crud = CRUDLogo()