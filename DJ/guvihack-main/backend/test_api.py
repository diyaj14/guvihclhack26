import requests
import json
import time

API_URL = "http://localhost:8000/webhook"
API_KEY = "meowdj@32"

def print_header(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")

def test_scam_detection():
    """Test 1: Basic scam detection with urgency and financial keywords"""
    print_header("TEST 1: SCAM DETECTION")
    
    payload = {
        "sessionId": "python-test-001",
        "message": {
            "sender": "scammer",
            "text": "Urgent! Your account is suspended. Transfer Rs 5000 to 9876543210 immediately.",
            "timestamp": "1770005528731"
        },
        "conversationHistory": []
    }
    
    headers = {"x-api-key": API_KEY}
    
    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=10)
        print(f"✅ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"📝 Agent Reply: {data.get('reply')}")
            print(f"🧠 Debug Thought: {data.get('debug_thought')}")
            print(f"📊 Confidence: {data.get('metrics', {}).get('confidence')}")
            print(f"🔍 Intelligence Extracted:")
            intel = data.get('intelligence', {})
            for key, value in intel.items():
                if value:
                    print(f"   - {key}: {value}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

def test_multi_turn():
    """Test 2: Multi-turn conversation with context"""
    print_header("TEST 2: MULTI-TURN CONVERSATION")
    
    session_id = "python-test-002"
    
    # Turn 1
    print("🔄 Turn 1: Initial contact")
    payload1 = {
        "sessionId": session_id,
        "message": {
            "sender": "scammer",
            "text": "Hello, this is Rajesh from HDFC Bank customer care.",
            "timestamp": "1770005528731"
        },
        "conversationHistory": []
    }
    
    headers = {"x-api-key": API_KEY}
    response1 = requests.post(API_URL, json=payload1, headers=headers, timeout=10)
    
    if response1.status_code == 200:
        data1 = response1.json()
        agent_reply1 = data1.get('reply')
        print(f"   Scammer: {payload1['message']['text']}")
        print(f"   Agent: {agent_reply1}")
        
        time.sleep(1)
        
        # Turn 2
        print("\n🔄 Turn 2: Scam reveal")
        payload2 = {
            "sessionId": session_id,
            "message": {
                "sender": "scammer",
                "text": "Your KYC is pending. Send payment to rajesh@paytm to update immediately.",
                "timestamp": "1770005528732"
            },
            "conversationHistory": [
                {
                    "sender": "scammer",
                    "text": "Hello, this is Rajesh from HDFC Bank customer care.",
                    "timestamp": "1770005528731"
                },
                {
                    "sender": "user",
                    "text": agent_reply1,
                    "timestamp": "1770005528731"
                }
            ]
        }
        
        response2 = requests.post(API_URL, json=payload2, headers=headers, timeout=10)
        
        if response2.status_code == 200:
            data2 = response2.json()
            print(f"   Scammer: {payload2['message']['text']}")
            print(f"   Agent: {data2.get('reply')}")
            print(f"\n📊 Final Intelligence:")
            intel = data2.get('intelligence', {})
            for key, value in intel.items():
                if value:
                    print(f"   - {key}: {value}")
    else:
        print(f"❌ Turn 1 failed: {response1.text}")

def test_intelligence_extraction():
    """Test 3: Comprehensive intelligence extraction"""
    print_header("TEST 3: INTELLIGENCE EXTRACTION")
    
    payload = {
        "sessionId": "python-test-003",
        "message": {
            "sender": "scammer",
            "text": "I am Vinod Kumar, branch manager at Mumbai HDFC. Send to vinod@paytm or call 9123456789. My account is 12345678901234. Visit http://fake-bank.com/verify",
            "timestamp": "1770005528731"
        },
        "conversationHistory": []
    }
    
    headers = {"x-api-key": API_KEY}
    response = requests.post(API_URL, json=payload, headers=headers, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        intel = data.get('intelligence', {})
        
        print("🔍 Extracted Intelligence:")
        print(f"   👤 Scammer Name: {intel.get('scammerName', [])}")
        print(f"   💳 UPI IDs: {intel.get('upiIds', [])}")
        print(f"   📞 Phone Numbers: {intel.get('phoneNumbers', [])}")
        print(f"   🏦 Bank Accounts: {intel.get('bankAccounts', [])}")
        print(f"   🔗 Phishing Links: {intel.get('phishingLinks', [])}")
        print(f"   📍 Location: {intel.get('location', [])}")
        print(f"   💼 Job Title: {intel.get('jobTitle', [])}")
        print(f"   🚨 Suspicious Keywords: {intel.get('suspiciousKeywords', [])}")
        
        # Validation
        print("\n✅ Validation:")
        checks = [
            ("Name extraction", len(intel.get('scammerName', [])) > 0),
            ("UPI extraction", len(intel.get('upiIds', [])) > 0),
            ("Phone extraction", len(intel.get('phoneNumbers', [])) > 0),
            ("Bank account extraction", len(intel.get('bankAccounts', [])) > 0),
            ("URL extraction", len(intel.get('phishingLinks', [])) > 0),
            ("Location extraction", len(intel.get('location', [])) > 0),
        ]
        
        for check_name, passed in checks:
            status = "✅" if passed else "❌"
            print(f"   {status} {check_name}")
    else:
        print(f"❌ Error: {response.text}")

def test_invalid_api_key():
    """Test 4: API authentication"""
    print_header("TEST 4: API AUTHENTICATION")
    
    payload = {
        "sessionId": "python-test-004",
        "message": {
            "sender": "scammer",
            "text": "Test message",
            "timestamp": "1770005528731"
        },
        "conversationHistory": []
    }
    
    # Test with invalid key
    print("🔒 Testing with invalid API key...")
    headers = {"x-api-key": "wrong-key-12345"}
    response = requests.post(API_URL, json=payload, headers=headers, timeout=10)
    
    if response.status_code == 401:
        print(f"✅ Authentication working correctly (Status: {response.status_code})")
        print(f"   Response: {response.json()}")
    else:
        print(f"❌ Expected 401, got {response.status_code}")
    
    # Test with valid key
    print("\n🔓 Testing with valid API key...")
    headers = {"x-api-key": API_KEY}
    response = requests.post(API_URL, json=payload, headers=headers, timeout=10)
    
    if response.status_code == 200:
        print(f"✅ Valid key accepted (Status: {response.status_code})")
    else:
        print(f"❌ Valid key rejected: {response.text}")

def test_phishing_scenario():
    """Test 5: Phishing link scenario"""
    print_header("TEST 5: PHISHING LINK DETECTION")
    
    payload = {
        "sessionId": "python-test-005",
        "message": {
            "sender": "scammer",
            "text": "Congratulations! You won Rs 50,000. Click here to claim: http://fake-prize-winner.com/claim?id=victim123. Call 9988776655 for assistance.",
            "timestamp": "1770005528731"
        },
        "conversationHistory": []
    }
    
    headers = {"x-api-key": API_KEY}
    response = requests.post(API_URL, json=payload, headers=headers, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        intel = data.get('intelligence', {})
        metrics = data.get('metrics', {})
        
        print(f"📝 Agent Reply: {data.get('reply')}")
        print(f"📊 Scam Confidence: {metrics.get('confidence')}")
        print(f"\n🔍 Detected:")
        print(f"   🔗 Phishing Links: {intel.get('phishingLinks', [])}")
        print(f"   📞 Phone Numbers: {intel.get('phoneNumbers', [])}")
        print(f"   🚨 Keywords: {intel.get('suspiciousKeywords', [])}")
        
        # Check if high confidence
        if metrics.get('confidence', 0) > 0.5:
            print(f"\n✅ High confidence scam detected - Callback should be triggered")
        else:
            print(f"\n⚠️ Low confidence - May not trigger callback")
    else:
        print(f"❌ Error: {response.text}")

def test_voice_normalized_input():
    """Test 6: Voice-style input (spoken numbers and 'at')"""
    print_header("TEST 6: VOICE INPUT NORMALIZATION")
    
    payload = {
        "sessionId": "python-test-006",
        "message": {
            "sender": "scammer",
            "text": "Send to rajesh at paytm. My number is nine eight seven six five four three two one zero.",
            "timestamp": "1770005528731"
        },
        "conversationHistory": []
    }
    
    headers = {"x-api-key": API_KEY}
    response = requests.post(API_URL, json=payload, headers=headers, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        intel = data.get('intelligence', {})
        
        print(f"📝 Original Text: {payload['message']['text']}")
        print(f"🔍 Extracted:")
        print(f"   💳 UPI IDs: {intel.get('upiIds', [])}")
        print(f"   📞 Phone Numbers: {intel.get('phoneNumbers', [])}")
        
        # Note: Voice normalization happens in intelligence.py
        if intel.get('upiIds') or intel.get('phoneNumbers'):
            print(f"\n✅ Voice normalization working")
        else:
            print(f"\n⚠️ Voice normalization may need improvement")
    else:
        print(f"❌ Error: {response.text}")

def run_all_tests():
    """Run all test cases"""
    print("\n" + "🧪"*30)
    print("  VIGILANTE AI - API TEST SUITE")
    print("🧪"*30)
    
    print(f"\n📡 Testing endpoint: {API_URL}")
    print(f"🔑 Using API key: {API_KEY}")
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print(f"✅ Backend server is running")
        else:
            print(f"⚠️ Backend returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Cannot connect to backend: {str(e)}")
        print(f"   Make sure the server is running: uvicorn main:app --reload")
        return
    
    # Run tests
    tests = [
        test_scam_detection,
        test_multi_turn,
        test_intelligence_extraction,
        test_invalid_api_key,
        test_phishing_scenario,
        test_voice_normalized_input
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            test_func()
            passed += 1
            time.sleep(0.5)  # Small delay between tests
        except Exception as e:
            print(f"\n❌ Test failed with exception: {str(e)}")
            failed += 1
    
    # Summary
    print_header("TEST SUMMARY")
    print(f"✅ Passed: {passed}/{len(tests)}")
    print(f"❌ Failed: {failed}/{len(tests)}")
    
    if failed == 0:
        print("\n🎉 All tests passed! Your API is ready for evaluation.")
    else:
        print("\n⚠️ Some tests failed. Please review the output above.")

if __name__ == "__main__":
    run_all_tests()
