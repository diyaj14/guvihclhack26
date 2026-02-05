# 🧪 Testing Guide - Vigilante AI Honey-Pot

## Quick Start Testing

### 1. Test with GUVI's Official Tester
The image you have shows GUVI's official API endpoint tester. Use these values:

**Headers:**
- `x-api-key`: `meowdj@32`

**Honeypot API Endpoint URL:**
- Local: `http://localhost:8000/webhook`
- Production: `https://your-deployed-url.com/webhook`

---

## 2. Manual Testing with cURL

### Test 1: Bank Fraud Scam (First Message)
```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -H "x-api-key: meowdj@32" \
  -d '{
    "sessionId": "test-session-001",
    "message": {
      "sender": "scammer",
      "text": "Your bank account will be blocked today. Verify immediately.",
      "timestamp": "1770005528731"
    },
    "conversationHistory": [],
    "metadata": {
      "channel": "SMS",
      "language": "English",
      "locale": "IN"
    }
  }'
```

**Expected Response:**
```json
{
  "status": "success",
  "reply": "oh dear... why would it be blocked?",
  "debug_thought": "Scammer using urgency tactics | Standard",
  "intelligence": {
    "bankAccounts": [],
    "upiIds": [],
    "phishingLinks": [],
    "phoneNumbers": [],
    "suspiciousKeywords": ["urgent", "blocked", "verify"]
  },
  "metrics": {
    "turns": 1,
    "confidence": 0.7
  }
}
```

---

### Test 2: UPI Scam (Follow-up Message)
```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -H "x-api-key: 12345" \
  -d '{
    "sessionId": "test-session-001",
    "message": {
      "sender": "scammer",
      "text": "Send money to scammer@paytm to verify your account. My name is Vinod from Delhi branch.",
      "timestamp": "1770005528731"
    },
    "conversationHistory": [
      {
        "sender": "scammer",
        "text": "Your bank account will be blocked today. Verify immediately.",
        "timestamp": "1770005528731"
      },
      {
        "sender": "user",
        "text": "oh dear... why would it be blocked?",
        "timestamp": "1770005528731"
      }
    ],
    "metadata": {
      "channel": "SMS",
      "language": "English",
      "locale": "IN"
    }
  }'
```

**Expected Response:**
```json
{
  "status": "success",
  "reply": "ok vinod... but the link isnt opening",
  "intelligence": {
    "scammerName": ["Vinod"],
    "upiIds": ["scammer@paytm"],
    "location": ["Delhi"],
    "jobTitle": ["Branch"],
    "suspiciousKeywords": ["verify", "account"]
  }
}
```

---

### Test 3: Phishing Link Scam
```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -H "x-api-key: 12345" \
  -d '{
    "sessionId": "test-session-002",
    "message": {
      "sender": "scammer",
      "text": "Click here to claim your prize: http://fake-bank-login.com/verify?id=12345. Call me at 9876543210 for help.",
      "timestamp": "1770005528731"
    },
    "conversationHistory": []
  }'
```

**Expected Intelligence Extraction:**
- `phishingLinks`: ["http://fake-bank-login.com/verify?id=12345"]
- `phoneNumbers`: ["9876543210"]
- `suspiciousKeywords`: ["click here", "prize"]

---

### Test 4: Invalid API Key (Should Fail)
```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -H "x-api-key: wrong-key" \
  -d '{
    "sessionId": "test-session-003",
    "message": {
      "sender": "scammer",
      "text": "Test message",
      "timestamp": "1770005528731"
    },
    "conversationHistory": []
  }'
```

**Expected Response:**
```json
{
  "detail": "Invalid API Key"
}
```

---

## 3. Python Test Script

Create a file `test_api.py`:

```python
import requests
import json

API_URL = "http://localhost:8000/webhook"
API_KEY = "12345"

def test_scam_detection():
    """Test 1: Basic scam detection"""
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
    response = requests.post(API_URL, json=payload, headers=headers)
    
    print("Test 1: Scam Detection")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("\n" + "="*50 + "\n")

def test_multi_turn():
    """Test 2: Multi-turn conversation"""
    # First message
    payload1 = {
        "sessionId": "python-test-002",
        "message": {
            "sender": "scammer",
            "text": "Hello, this is Rajesh from HDFC Bank customer care.",
            "timestamp": "1770005528731"
        },
        "conversationHistory": []
    }
    
    headers = {"x-api-key": API_KEY}
    response1 = requests.post(API_URL, json=payload1, headers=headers)
    agent_reply = response1.json()["reply"]
    
    # Second message (with history)
    payload2 = {
        "sessionId": "python-test-002",
        "message": {
            "sender": "scammer",
            "text": "Your KYC is pending. Send payment to rajesh@paytm to update.",
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
                "text": agent_reply,
                "timestamp": "1770005528731"
            }
        ]
    }
    
    response2 = requests.post(API_URL, json=payload2, headers=headers)
    
    print("Test 2: Multi-Turn Conversation")
    print(f"Turn 1 Reply: {agent_reply}")
    print(f"Turn 2 Response: {json.dumps(response2.json(), indent=2)}")
    print("\n" + "="*50 + "\n")

def test_intelligence_extraction():
    """Test 3: Intelligence extraction"""
    payload = {
        "sessionId": "python-test-003",
        "message": {
            "sender": "scammer",
            "text": "I am Vinod Kumar, branch manager at Mumbai. Send to vinod@paytm or call 9123456789. Account: 12345678901234",
            "timestamp": "1770005528731"
        },
        "conversationHistory": []
    }
    
    headers = {"x-api-key": API_KEY}
    response = requests.post(API_URL, json=payload, headers=headers)
    intel = response.json().get("intelligence", {})
    
    print("Test 3: Intelligence Extraction")
    print(f"Scammer Name: {intel.get('scammerName', [])}")
    print(f"UPI IDs: {intel.get('upiIds', [])}")
    print(f"Phone Numbers: {intel.get('phoneNumbers', [])}")
    print(f"Bank Accounts: {intel.get('bankAccounts', [])}")
    print(f"Location: {intel.get('location', [])}")
    print(f"Job Title: {intel.get('jobTitle', [])}")
    print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    print("🧪 Starting API Tests...\n")
    test_scam_detection()
    test_multi_turn()
    test_intelligence_extraction()
    print("✅ All tests completed!")
```

Run with:
```bash
python test_api.py
```

---

## 4. Postman Collection

Import this JSON into Postman:

```json
{
  "info": {
    "name": "Vigilante AI Honey-Pot Tests",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Test 1: Bank Fraud",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "x-api-key",
            "value": "12345"
          },
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"sessionId\": \"postman-test-001\",\n  \"message\": {\n    \"sender\": \"scammer\",\n    \"text\": \"Your account is suspended. Verify now or face legal action.\",\n    \"timestamp\": \"1770005528731\"\n  },\n  \"conversationHistory\": []\n}"
        },
        "url": {
          "raw": "http://localhost:8000/webhook",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["webhook"]
        }
      }
    }
  ]
}
```

---

## 5. Sample Scam Messages for Testing

### High-Confidence Scams (Should trigger callback)

1. **Bank Fraud:**
   - "Your account will be blocked. Transfer to 9876543210 immediately."
   - "KYC update required. Send to manager@paytm now."

2. **Prize/Lottery:**
   - "Congratulations! You won Rs 50,000. Click http://fake-prize.com to claim."
   - "You are selected for cashback. Share UPI ID urgently."

3. **Tech Support:**
   - "Your computer has virus. Call 1800-SCAM-NOW immediately."
   - "Microsoft detected unauthorized access. Download fix: http://malware.com"

4. **Tax/Legal:**
   - "Income tax refund pending. Verify at http://fake-tax.com"
   - "Legal notice issued. Pay fine to advocate@upi immediately."

### Medium-Confidence (Should engage cautiously)

1. "Hello, this is customer care calling."
2. "We have an offer for you. Interested?"
3. "Your delivery is pending. Confirm address."

### Low-Confidence (Should still engage in honeypot mode)

1. "Hi, how are you?"
2. "Can you help me with something?"

---

## 6. Expected Behavior Checklist

### ✅ Scam Detection
- [ ] Detects urgency keywords (urgent, immediately, blocked)
- [ ] Detects financial keywords (pay, transfer, UPI, bank)
- [ ] Detects suspicious actions (click here, download)
- [ ] Returns confidence score (0.0-1.0)

### ✅ Intelligence Extraction
- [ ] Extracts UPI IDs (format: name@bank)
- [ ] Extracts phone numbers (Indian format)
- [ ] Extracts bank accounts (11-18 digits)
- [ ] Extracts URLs
- [ ] Extracts scammer names
- [ ] Extracts locations
- [ ] Extracts job titles
- [ ] Extracts suspicious keywords

### ✅ Agent Behavior
- [ ] Responds in character (Mrs. Higgins or Ramesh)
- [ ] Keeps responses under 12 words
- [ ] Uses lowercase, informal language
- [ ] Doesn't repeat questions (context-aware)
- [ ] Varies strategies (tech errors, distractions)

### ✅ Multi-Turn Handling
- [ ] Maintains conversation context
- [ ] Accumulates intelligence across turns
- [ ] Adapts strategy based on phase (ENGAGEMENT vs EXTRACTION)

### ✅ Callback
- [ ] Sends callback when confidence > 0.4
- [ ] Includes all required fields (sessionId, scamDetected, etc.)
- [ ] Includes extracted intelligence
- [ ] Includes agent notes with confidence score

---

## 7. Monitoring Callback Execution

Check your backend logs for:

```
Callback Payload (Mock Sent): {
  "sessionId": "test-session-001",
  "scamDetected": true,
  "totalMessagesExchanged": 3,
  "extractedIntelligence": {
    "bankAccounts": ["12345678901234"],
    "upiIds": ["scammer@paytm"],
    "phishingLinks": [],
    "phoneNumbers": ["9876543210"],
    "suspiciousKeywords": ["urgent", "verify", "blocked"]
  },
  "agentNotes": "Scam Confidence: 0.8 (Urgency/Threat detected, Financial request detected) | Strategy: Tech Error"
}
```

---

## 8. Testing the Voice Agent

1. **Start the voice agent:**
   ```bash
   cd C:\guvihackfinal\guvihclhack26\Phase3_Voice
   python agent/agent.py dev
   ```

2. **Open the frontend:**
   ```bash
   cd C:\guvihackfinal\guvihclhack26\DJ\guvihack-main\frontend
   npm run dev
   ```

3. **Navigate to:** `http://localhost:3000`

4. **Test voice scenarios:**
   - "Hello, this is bank manager calling"
   - "Your account is suspended, send money to nine eight seven six at paytm"
   - "Click the link I sent for verification"

---

## 9. Common Issues & Fixes

### Issue: "Invalid API Key"
**Fix:** Ensure header is `x-api-key: 12345`

### Issue: No callback in logs
**Fix:** Check confidence score. Callback only triggers if `confidence > 0.4` or `is_scam = true`

### Issue: Empty intelligence
**Fix:** Use more explicit scam messages with UPI IDs, phone numbers, or URLs

### Issue: Agent repeats questions
**Fix:** Ensure `conversationHistory` is properly populated in follow-up messages

---

## 10. Performance Benchmarks

**Expected Response Times:**
- First message: < 2 seconds
- Follow-up messages: < 1.5 seconds
- Intelligence extraction: < 500ms
- Callback execution: < 1 second (background task)

**Scam Detection Accuracy:**
- High-confidence scams: > 90% detection rate
- Medium-confidence: > 70% detection rate
- False positives: < 5%

---

## Ready to Test! 🚀

Start with the cURL commands, then move to the Python script for automated testing. Use the GUVI official tester for final validation before submission.
