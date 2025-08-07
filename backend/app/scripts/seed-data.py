# scripts/seed_data.py

import asyncio
import datetime
import decimal
import json
from pathlib import Path
import uuid as uuid_pkg
import pandas as pd
from sqlmodel import delete, select
from app.db.database import AsyncSessionLocal
from app.models import (
    BusinessUser,
    LoyaltyProgram,
    Order,
    User,
    AnalysisResult,
    ChatMessage
)

# --- CONFIGURATION: UPDATE THESE PATHS ---
# Place your CSV files in a 'data' folder in your project root, for example.
DATA_DIR = Path(__file__).parent.parent / "data"
SIP_Latte_CSV = DATA_DIR / "sip_Latte_orders.csv"
MAKERS_SHAKE_CSV = DATA_DIR / "makers_of_milkshake_orders.csv"
# -----------------------------------------


def clean_data_for_json(row: pd.Series) -> dict:
    """Converts a pandas row to a JSON-serializable dictionary."""
    # Convert numpy types to native Python types
    native_dict = row.to_dict()
    for key, value in native_dict.items():
        if pd.isna(value):
            native_dict[key] = None
        elif isinstance(value, (pd.Timestamp, datetime.datetime, datetime.date)):
            native_dict[key] = value.isoformat()
        elif isinstance(value, (int, float, bool, str)) or value is None:
            continue
        else:
            native_dict[key] = str(value) # Fallback to string for other types
    return native_dict


async def seed_data():
    print("🌱 Starting database seeding from CSV files...")
    
    async with AsyncSessionLocal() as session:
        # 1. Clear existing data
        print("   - Clearing old data...")
        await session.exec(delete(AnalysisResult))
        await session.exec(delete(ChatMessage))
        await session.exec(delete(Order))
        await session.exec(delete(BusinessUser))
        await session.exec(delete(User))
        await session.exec(delete(LoyaltyProgram))
        await session.commit()

        # 2. Create Loyalty Programs and fake Users/BusinessUsers
        print("   - Creating base user and company data...")
        lp1 = LoyaltyProgram(brand_name="Sip-Latter", status_id=1, uuid=uuid_pkg.uuid4())
        lp2 = LoyaltyProgram(brand_name="Makers of Milkshake", status_id=1, uuid=uuid_pkg.uuid4())
        user1 = User(phone="1111111111", name="Sip-Latter Owner", uuid=uuid_pkg.uuid4())
        user2 = User(phone="2222222222", name="Makers Shake Owner", uuid=uuid_pkg.uuid4())
        session.add_all([lp1, lp2, user1, user2])
        await session.commit()

        # Refresh objects to get their generated IDs
        for obj in [lp1, lp2, user1, user2]:
            await session.refresh(obj)

        bu1 = BusinessUser(name="Sip-Latte Main", phone="1111111111", loyalty_program_id=lp1.id, store_details={})
        bu2 = BusinessUser(name="Makers Shake Main", phone="2222222222", loyalty_program_id=lp2.id, store_details={})
        session.add_all([bu1, bu2])
        await session.commit()
        
        # 3. Process CSVs and create Order records
        cafes_to_process = [
            {"loyalty_program": lp1, "user": user1, "file_path": SIP_Latte_CSV},
            {"loyalty_program": lp2, "user": user2, "file_path": MAKERS_SHAKE_CSV},
        ]

        for cafe in cafes_to_process:
            lp = cafe["loyalty_program"]
            file_path = cafe["file_path"]
            print(f"   - Processing orders for: {lp.brand_name} from {file_path.name}")
            
            if not file_path.exists():
                print(f"     - ⚠️ WARNING: CSV file not found, skipping. Path: {file_path}")
                continue

            try:
                df = pd.read_csv(file_path)
                # Ensure date column is parsed correctly
                if 'date' in df.columns:
                    df['date'] = pd.to_datetime(df['date'], errors='coerce')
                
                orders_to_add = []
                for index, row in df.iterrows():
                    raw_pos_data = clean_data_for_json(row)
                    
                    order = Order(
                        # Extract key fields for top-level columns
                        order_id=str(row.get("invoice_no", f"ORD-{lp.id}-{index}")),
                        rest_id=str(lp.id),
                        total_amount=decimal.Decimal(str(row.get("total", 0))),
                        order_date=row.get('date'),
                        pos_raw_data=raw_pos_data,  # Store the entire row as JSON
                        
                        # Link to the correct loyalty program and a user
                        loyalty_program_id=lp.id,
                        user_id=cafe["user"].id
                    )
                    orders_to_add.append(order)
                
                session.add_all(orders_to_add)
                await session.commit()
                print(f"     - ✅ Successfully seeded {len(orders_to_add)} orders.")

            except Exception as e:
                print(f"     - ❌ ERROR processing file {file_path.name}: {e}")

    print("✅ Database seeding completed!")

if __name__ == "__main__":
    asyncio.run(seed_data())