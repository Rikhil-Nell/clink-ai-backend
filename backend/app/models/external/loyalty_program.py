import uuid as uuid_pkg
from datetime import datetime, timezone
from typing import List, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .business_user import BusinessUser
    from .order import Order

class LoyaltyProgram(SQLModel, table=True):
    __tablename__ = "loyalty_programs"
    id: uuid_pkg.UUID = Field(default_factory=uuid_pkg.uuid4, primary_key=True, index=True)
    brand_name: str
    status_id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Forward references using strings
    business_users: List["BusinessUser"] = Relationship(back_populates="loyalty_program")
    orders: List["Order"] = Relationship(back_populates="loyalty_program")