import os
import sys
from dotenv import load_dotenv
from livekit import api

# Load environment variables
load_dotenv()

def generate_token():
    api_key = os.getenv("LIVEKIT_API_KEY")
    api_secret = os.getenv("LIVEKIT_API_SECRET")

    if not api_key or not api_secret:
        print("Error: LIVEKIT_API_KEY or LIVEKIT_API_SECRET not found in .env")
        return

    # Create an Access Token
    token = api.AccessToken(api_key, api_secret) \
        .with_identity("scammer_identity") \
        .with_name("Scammer Caller") \
        .with_grants(api.VideoGrants(room_join=True, room="test-room", can_update_own_metadata=True))

    jwt_token = token.to_jwt()
    print("\n" + "="*50)
    print("GENERATED LIVEKIT TOKEN")
    print("="*50)
    print(jwt_token)
    print("="*50 + "\n")
    print("👉 Copy the token above and paste it into 'Phase3_Voice/frontend_demo/index.html' inside const TOKEN = '...'")

if __name__ == "__main__":
    try:
        generate_token()
    except Exception as e:
        print(f"Error generating token: {e}")
        print("Make sure 'livekit-server-sdk' or 'livekit-api' is installed via requirements.")
