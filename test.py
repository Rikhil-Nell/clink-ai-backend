import asyncio
import redis.asyncio as redis
import json
from dotenv import load_dotenv
load_dotenv()
import os
# --- CONFIGURATION ---
# 1. Paste your Redis connection URL here.
#    (This should be the same as the REDIS_URL in your .env file)
REDIS_URL = os.getenv("REDIS_URL")

# 2. Paste the testing token you were given.
TEST_TOKEN = "8KOGh4ym5dyv0VsWIoQKmcIr3qjI7Z0nmlCkIFZPExsTGoNxyrxj--8cZYvewdiwC5DkVLNg2zPmQrX5vvCNbJYmgKCzkeDx6bHI_019BHLPvqwFW1KX11qSg-vElUVzYy110kU-1I_k-CoUVIW7V_wz_04S_FxhTR0HaqnnyLk"


async def main():
    """
    Connects to Redis, fetches the value for the test token, and prints it.
    """
    print("--- Redis Test Script ---")
    
    try:
        # Create an asynchronous Redis client
        redis_client = redis.from_url(REDIS_URL, decode_responses=True)
        
        # Construct the key exactly as your application does
        redis_key = f"business_user_token:{TEST_TOKEN}"
        
        print(f"Connecting to Redis at: {REDIS_URL}")
        print(f"Querying for key: '{redis_key}'")
        
        # Fetch the value from Redis
        value_str = await redis_client.get(redis_key)
        
        print("-" * 25)
        
        if value_str:
            print("✅ Token FOUND in Redis.")
            print(f"   Raw value: {value_str}")
            
            # Try to parse the value as JSON, as your app expects
            try:
                parsed_data = json.loads(value_str)
                print("   Successfully parsed JSON data:")
                print(f"   Value Str: {parsed_data}")
            except json.JSONDecodeError:
                print("   ⚠️  Warning: The value found is not a valid JSON string.")
                
        else:
            print("❌ Token NOT FOUND in Redis.")
            
        print("-" * 25)

    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        if 'redis_client' in locals():
            await redis_client.aclose()
            print("Connection closed.")


if __name__ == "__main__":
    asyncio.run(main())