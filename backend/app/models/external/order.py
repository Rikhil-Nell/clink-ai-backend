import uuid as uuid_pkg
import decimal
from datetime import datetime, timezone
from typing import Optional, Dict, Any, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column

if TYPE_CHECKING:
    from .user import User
    from .loyalty_program import LoyaltyProgram

class Order(SQLModel, table=True):
    __tablename__ = "orders"
    id: uuid_pkg.UUID = Field(default_factory=uuid_pkg.uuid4, primary_key=True, index=True)
    order_id: str
    total_amount: Optional[decimal.Decimal] = None
    order_date: Optional[datetime] = None
    pos_raw_data: Dict[str, Any] = Field(default_factory=dict,sa_column=Column(JSONB))
    loyalty_program_id: uuid_pkg.UUID = Field(foreign_key="loyalty_programs.id")
    user_id: Optional[uuid_pkg.UUID] = Field(default=None, foreign_key="users.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Forward references using strings
    user: Optional["User"] = Relationship(back_populates="orders")
    loyalty_program: "LoyaltyProgram" = Relationship(back_populates="orders")