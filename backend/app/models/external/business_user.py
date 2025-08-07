import uuid as uuid_pkg
from datetime import datetime, timezone
from typing import Dict, Any, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column

if TYPE_CHECKING:
    from .loyalty_program import LoyaltyProgram
    
class BusinessUser(SQLModel, table=True):
    __tablename__ = "business_users"
    id: uuid_pkg.UUID = Field(default_factory=uuid_pkg.uuid4, primary_key=True, index=True)
    name: str
    phone: str
    store_details: Dict[str, Any] = Field(default_factory=dict,sa_column=Column(JSONB))
    loyalty_program_id: uuid_pkg.UUID = Field(foreign_key="loyalty_programs.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Forward reference using a string
    loyalty_program: "LoyaltyProgram" = Relationship(back_populates="business_users")