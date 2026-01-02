from app.agents.registry import get_agent
from app.services.s3_service import get_presigned_url, upload_file, generate_coupon_key
from app.crud.logo_crud import logo_crud
from app.schemas.core.image_gen import CouponImageRequest, CouponImageResponse

import asyncpg
from uuid import UUID
from pydantic_ai import ImageUrl, BinaryImage


def _build_stencil_prompt(request: CouponImageRequest) -> str:
    """
    Build the stencil/layout prompt.
    This creates a structural blueprint for the coupon.
    """
    colors_hint = ", ".join(request.brand_colors) if request.brand_colors else "brand-appropriate warm colors"
    
    # Determine primary product based on brand or let AI decide
    product_suggestions = "milkshake cup, coffee cup, dessert plate, food packaging, or branded container"
    
    return f"""Design a coupon layout for: {request.brand_name}

COUPON CONTENT:
- Main Discount: "{request.discount_text}" (make this the LARGEST, most prominent)
- Validity: "{request.validity_text}"
- Offer Type: {request.selected_offer.template_name.replace('_', ' ').title()}

COMPOSITION REQUIREMENTS:
- Feature appetizing food/beverage as the hero element
- Include a product with a natural surface for logo placement ({product_suggestions})
- Position discount text prominently - right side or overlaying a dark/contrasting area
- Smaller validity text below or near the discount
- Style: {request.style_config.style}
- Mood: {request.style_config.mood}
- Color palette: {colors_hint}

LAYOUT STYLE:
- {"Hero food/beverage product with scattered ingredients/toppings around it" if request.style_config.include_food_imagery else "Clean minimal composition with subtle product focus"}
- Dark, rich background for contrast (like the wooden/dark surface style)
- Text on the right side with clear readability
- Product (with logo surface) on the left/center

Create a structural layout showing this composition."""


def _build_coupon_prompt(request: CouponImageRequest) -> str:
    """
    Build the full coupon render prompt.
    """
    colors_str = ", ".join(request.brand_colors) if request.brand_colors else "rich, appetizing colors matching the brand"
    
    # Eligibility-specific visual hints
    eligibility = request.selected_offer.variant_data.eligibility
    visual_hint = ""
    if eligibility.kind == "visit_milestone":
        visual_hint = "Add a subtle celebratory feel - this is a loyalty reward achievement."
    elif eligibility.kind == "first_visit":
        visual_hint = "Make it welcoming and inviting - this greets new customers."
    elif eligibility.kind == "winback":
        visual_hint = "Warm and nostalgic feel - we're welcoming them back."
    elif eligibility.kind == "time_based":
        visual_hint = "Energetic happy hour vibe - convey limited-time value."
    elif eligibility.kind == "stamp_card":
        visual_hint = "Rewarding, collectible feel - they've earned this."
    
    return f"""Generate a premium coupon image for {request.brand_name}.

RENDER THIS TEXT EXACTLY:
- Discount: "{request.discount_text}" (LARGEST - like "Flat 50%" style)
- Validity: "{request.validity_text}" (smaller, below discount)

LOGO PLACEMENT:
- Place the provided logo ON a product surface (cup, container, packaging)
- Make it look printed/part of the product, NOT a floating overlay
- Size appropriately for the product surface

VISUAL REQUIREMENTS:
- Style: {request.style_config.style}
- Mood: {request.style_config.mood}  
- Colors: {colors_str}
- Dark, rich background (wood, dark surface) for premium feel
- Appetizing hero product (beverage/food) as the central element
- {"Scattered ingredients, toppings, or garnishes around the hero product" if request.style_config.include_food_imagery else "Clean, minimal composition"}
- Professional food photography aesthetic
- {visual_hint}

TEXT STYLING:
- Discount text: Large, elegant serif or display font (cream/warm white color)
- "off" or connecting words: Smaller, same style
- Validity text: Clean, readable, smaller size
- Text positioned on the right side with good contrast

QUALITY: High-end marketing material suitable for social media and print."""


async def _generate_stencil(user_prompt: str, logo_link: str) -> BinaryImage:
    """Generate the layout/stencil using the stencil agent."""
    try:
        print(f"DEBUG: Getting stencil agent...")
        agent = get_agent(agent_type="stencil", agent_category="stencil")
        print(f"DEBUG: Agent retrieved: {agent}")
        print(f"DEBUG: Logo link: {logo_link[:100]}...")
        print(f"DEBUG: Prompt length: {len(user_prompt)}")
        
        print(f"DEBUG: Running agent...")
        result = await agent.run(user_prompt=[
            user_prompt, 
            ImageUrl(url=logo_link),
        ])
        print(f"DEBUG: Agent run complete, result type: {type(result)}")
        print(f"DEBUG: Output type: {type(result.output)}")
        return result.output
    except Exception as e:
        print(f"DEBUG ERROR in _generate_stencil: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        raise


async def _generate_coupon_image(
    user_prompt: str, 
    logo_link: str, 
    stencil_image: BinaryImage
) -> BinaryImage:
    """Generate the full coupon image using the image generation agent."""
    agent = get_agent(agent_type="image_generation", agent_category="image_generation")
    result = await agent.run(user_prompt=[
        user_prompt, 
        ImageUrl(url=logo_link),
        stencil_image
    ])
    return result.output


async def _fetch_logo(pool: asyncpg.Pool, loyalty_program_id: int) -> str:
    """Fetch logo presigned URL from S3 using ActiveStorage mapping."""
    logo_info = await logo_crud.get_logo_key_for_loyalty_program(pool, loyalty_program_id)
    if logo_info:
        return get_presigned_url(logo_info.key)
    return None


async def _upload_image(
    loyalty_program_id: int, 
    order_id: UUID, 
    image: BinaryImage, 
    offer_variant: str
) -> tuple[str, str]:
    """Upload image to S3 and return (url, key)."""
    key = generate_coupon_key(
        loyalty_program_id=loyalty_program_id, 
        order_id=order_id, 
        offer_variant=offer_variant
    )
    image_url = upload_file(file_data=image.data, key=key, content_type="image/png")
    return image_url, key
    # upload_file(file_data=image.data, key=key, content_type="image/png")
    # return key


async def generate_coupon_image(
    pool: asyncpg.Pool,
    request: CouponImageRequest,
    loyalty_program_id: int,  # Now passed separately from auth
) -> CouponImageResponse:
    """
    Main entry point for coupon image generation.
    
    Flow:
    1. Fetch brand logo from S3
    2. Generate stencil/layout (Pass 1)
    3. Generate full coupon image using stencil (Pass 2)
    4. Upload to S3
    5. Return response
    """
    # Step 1: Fetch logo
    logo_link = await _fetch_logo(pool=pool, loyalty_program_id=loyalty_program_id)
    if not logo_link:
        raise ValueError(f"No logo found for loyalty_program_id: {loyalty_program_id}")
    
    # Step 2: Generate stencil
    stencil_prompt = _build_stencil_prompt(request)
    stencil_image = await _generate_stencil(user_prompt=stencil_prompt, logo_link=logo_link)
    
    print("DEBUG: Stencil Generated")
    # Step 3: Generate full coupon image
    coupon_prompt = _build_coupon_prompt(request)
    coupon_image = await _generate_coupon_image(
        user_prompt=coupon_prompt, 
        logo_link=logo_link, 
        stencil_image=stencil_image
    )
    
    # Step 4: Upload to S3 using auth-provided loyalty_program_id
    image_url, s3_key = await _upload_image(
    # s3_key = await _upload_image(    
        loyalty_program_id=loyalty_program_id,  # From auth
        order_id=request.order_id, 
        image=coupon_image, 
        offer_variant=request.offer_variant
    )
    print("DEBUG: Image Uploaded")
    return CouponImageResponse(
        image_url=image_url,
        s3_key=s3_key,
        discount_text=request.discount_text,
        validity_text=request.validity_text
    )