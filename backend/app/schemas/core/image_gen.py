from typing import Optional, Literal
from pydantic import BaseModel, Field, model_validator
from uuid import UUID

from app.schemas.offers.offer_variant import SelectedOfferVariant


class ImageStyleConfig(BaseModel):
    """
    Configuration for image generation style.
    Keep this minimal - most settings won't dramatically change output.
    """
    style: Literal["modern", "vintage", "minimal", "playful", "elegant", "bold"] = "modern"
    mood: Literal["warm", "cool", "neutral", "vibrant"] = "warm"
    include_food_imagery: bool = True  # Whether to include food/beverage graphics


class CouponImageRequest(BaseModel):
    """Request model for coupon image generation."""
    
    # === Required identifiers ===
    # loyalty_program_id: int = Field(..., description="ID to fetch logo and brand info")
    order_id: UUID = Field(..., description="The ai_suggestions row UUID")
    
    # === Offer details (from frontend selection) ===
    selected_offer: SelectedOfferVariant = Field(
        ..., 
        description="The specific offer variant selected for image generation"
    )
    
    # === Brand info (frontend provides or we fetch) ===
    brand_name: str = Field(..., description="Name of the cafe/restaurant")
    brand_colors: Optional[list[str]] = Field(
        default=None, 
        description="Brand colors as hex codes, e.g., ['#FF5733', '#FFFFFF']"
    )
    
    # === Optional style configuration ===
    style_config: ImageStyleConfig = Field(default_factory=ImageStyleConfig)
    
    # === Computed fields (populated from selected_offer) ===
    @property
    def discount_text(self) -> str:
        """Auto-generate discount text from the selected offer."""
        return self.selected_offer.get_discount_text()
    
    @property
    def validity_text(self) -> str:
        """Auto-generate validity text from eligibility criteria."""
        return self.selected_offer.get_eligibility_text()
    
    @property
    def offer_variant(self) -> str:
        """Return the variant type for S3 key generation."""
        return self.selected_offer.variant_type


class CouponImageResponse(BaseModel):
    """Result of coupon image generation."""
    image_url: str
    s3_key: str
    discount_text: str  # Echo back what was rendered
    validity_text: str