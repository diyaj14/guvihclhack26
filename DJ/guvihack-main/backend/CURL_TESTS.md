# 🧪 cURL Test Commands - Copy & Paste Ready

## Test 1: Basic Scam Detection
```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -H "x-api-key: 12345" \
  -d "{\"sessionId\": \"curl-test-001\", \"message\": {\"sender\": \"scammer\", \"text\": \"Your bank account will be blocked. Verify immediately.\", \"timestamp\": \"1770005528731\"}, \"conversationHistory\": []}"
```

## Test 2: UPI + Phone Extraction
```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -H "x-api-key: 12345" \
  -d "{\"sessionId\": \"curl-test-002\", \"message\": {\"sender\": \"scammer\", \"text\": \"I am Vinod from Mumbai. Send to vinod@paytm or call 9876543210.\", \"timestamp\": \"1770005528731\"}, \"conversationHistory\": []}"
```

## Test 3: Phishing Link
```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -H "x-api-key: 12345" \
  -d "{\"sessionId\": \"curl-test-003\", \"message\": {\"sender\": \"scammer\", \"text\": \"Click here to claim prize: http://fake-bank.com/verify\", \"timestamp\": \"1770005528731\"}, \"conversationHistory\": []}"
```

## Test 4: Multi-Turn Conversation (Turn 1)
```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -H "x-api-key: 12345" \
  -d "{\"sessionId\": \"curl-test-004\", \"message\": {\"sender\": \"scammer\", \"text\": \"Hello, this is customer care.\", \"timestamp\": \"1770005528731\"}, \"conversationHistory\": []}"
```

## Test 5: Multi-Turn Conversation (Turn 2)
**Note:** Replace `AGENT_REPLY_FROM_TURN_1` with actual reply from Test 4
```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -H "x-api-key: 12345" \
  -d "{\"sessionId\": \"curl-test-004\", \"message\": {\"sender\": \"scammer\", \"text\": \"Your KYC is pending. Send to support@paytm.\", \"timestamp\": \"1770005528732\"}, \"conversationHistory\": [{\"sender\": \"scammer\", \"text\": \"Hello, this is customer care.\", \"timestamp\": \"1770005528731\"}, {\"sender\": \"user\", \"text\": \"AGENT_REPLY_FROM_TURN_1\", \"timestamp\": \"1770005528731\"}]}"
```

## Test 6: Invalid API Key (Should Fail)
```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -H "x-api-key: wrong-key" \
  -d "{\"sessionId\": \"curl-test-005\", \"message\": {\"sender\": \"scammer\", \"text\": \"Test\", \"timestamp\": \"1770005528731\"}, \"conversationHistory\": []}"
```

## Test 7: Check Server Status
```bash
curl http://localhost:8000/
```

## PowerShell Version (Windows)

### Test 1: Basic Scam Detection
```powershell
$headers = @{
    "Content-Type" = "application/json"
    "x-api-key" = "12345"
}

$body = @{
    sessionId = "ps-test-001"
    message = @{
        sender = "scammer"
        text = "Your bank account will be blocked. Verify immediately."
        timestamp = "1770005528731"
    }
    conversationHistory = @()
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/webhook" -Method Post -Headers $headers -Body $body
```

### Test 2: UPI + Phone Extraction
```powershell
$headers = @{
    "Content-Type" = "application/json"
    "x-api-key" = "12345"
}

$body = @{
    sessionId = "ps-test-002"
    message = @{
        sender = "scammer"
        text = "I am Vinod from Mumbai. Send to vinod@paytm or call 9876543210."
        timestamp = "1770005528731"
    }
    conversationHistory = @()
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/webhook" -Method Post -Headers $headers -Body $body
```

## Expected Response Format

```json
{
  "status": "success",
  "reply": "oh dear... why would it be blocked?",
  "debug_thought": "Scammer using urgency tactics | Standard",
  "intelligence": {
    "scammerName": [],
    "bankAccounts": [],
    "upiIds": [],
    "phishingLinks": [],
    "phoneNumbers": [],
    "jobTitle": [],
    "companyNames": [],
    "location": [],
    "suspiciousKeywords": ["blocked", "verify"]
  },
  "metrics": {
    "turns": 1,
    "confidence": 0.7
  }
}
```

## Quick Python Test

```bash
python quick_test.py
```

## Full Test Suite

```bash
python test_api.py
```
