# Quick API Test - Single Request

import requests
import json

# Configuration
API_URL = "http://localhost:8000/webhook"
API_KEY = "meowdj@32"  # Updated API key for hackathon submission

# Test payload
payload = {
    "sessionId": "quick-test-001",
    "message": {
        "sender": "scammer",
        "text": "Your bank account will be blocked. Send money to scammer@paytm immediately. Call 9876543210.",
        "timestamp": "1770005528731"
    },
    "conversationHistory": []
}

headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

print("🧪 Testing Vigilante AI API...")
print(f"📡 Endpoint: {API_URL}")
print(f"🔑 API Key: {API_KEY}")
print(f"📝 Scam Message: {payload['message']['text']}\n")

try:
    response = requests.post(API_URL, json=payload, headers=headers, timeout=10)
    
    print(f"✅ Status Code: {response.status_code}\n")
    
    if response.status_code == 200:
        data = response.json()
        
        print("=" * 60)
        print("RESPONSE:")
        print("=" * 60)
        print(json.dumps(data, indent=2))
        
        print("\n" + "=" * 60)
        print("INTELLIGENCE EXTRACTED:")
        print("=" * 60)
        intel = data.get('intelligence', {})
        for key, value in intel.items():
            if value:
                print(f"  {key}: {value}")
        
        print("\n" + "=" * 60)
        print("METRICS:")
        print("=" * 60)
        metrics = data.get('metrics', {})
        print(f"  Turns: {metrics.get('turns')}")
        print(f"  Confidence: {metrics.get('confidence')}")
        
        if metrics.get('confidence', 0) > 0.4:
            print("\n✅ HIGH CONFIDENCE SCAM - Callback will be triggered!")
        
    else:
        print(f"❌ Error Response:")
        print(response.text)
        
except requests.exceptions.ConnectionError:
    print("❌ Cannot connect to backend!")
    print("   Make sure the server is running:")
    print("   cd C:\\guvihackfinal\\guvihclhack26\\DJ\\guvihack-main\\backend")
    print("   uvicorn main:app --reload")
except Exception as e:
    print(f"❌ Error: {str(e)}")
