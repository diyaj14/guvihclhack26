import requests
import json

# Your deployed API
API_URL = "https://guvihclhack26.onrender.com/webhook"
API_KEY = "meowdj@32"

print("🧪 Testing Deployed Vigilante AI API on Render...")
print(f"📡 Endpoint: {API_URL}\n")

# Test payload
payload = {
    "sessionId": "render-test-001",
    "message": {
        "sender": "scammer",
        "text": "Your bank account will be blocked. Send money to scammer@paytm immediately. Call 9876543210.",
        "timestamp": 1770005528731
    },
    "conversationHistory": []
}

headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

print(f"📝 Test Message: {payload['message']['text']}\n")
print("⏳ Sending request to deployed API...\n")

try:
    response = requests.post(API_URL, json=payload, headers=headers, timeout=30)
    
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
            print("\n✅ HIGH CONFIDENCE SCAM - Callback triggered!")
        
        print("\n🎉 DEPLOYMENT SUCCESSFUL! Your API is live and working!")
        
    elif response.status_code == 401:
        print("❌ Authentication failed!")
        print(f"   Response: {response.text}")
        print("   Check that API key is correct: meowdj@32")
    else:
        print(f"❌ Error Response (Status {response.status_code}):")
        print(response.text)
        
except requests.exceptions.Timeout:
    print("⏰ Request timed out (30s)")
    print("   This might be a cold start - try again in a moment")
except requests.exceptions.ConnectionError:
    print("❌ Cannot connect to deployed API!")
    print("   Check if the Render service is running")
except Exception as e:
    print(f"❌ Error: {str(e)}")

print("\n" + "=" * 60)
print("GUVI TESTER CONFIGURATION:")
print("=" * 60)
print(f"Honeypot API Endpoint URL: {API_URL}")
print(f"x-api-key: {API_KEY}")
print("=" * 60)
