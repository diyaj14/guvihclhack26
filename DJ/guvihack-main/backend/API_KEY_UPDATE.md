# ✅ API Key Updated to: meowdj@32

## Changes Made

The API key has been updated from `12345` to `meowdj@32` in the following files:

### ✅ Backend Code
- **main.py** - API validation logic updated

### ✅ Test Scripts
- **quick_test.py** - API_KEY constant updated
- **test_api.py** - API_KEY constant updated

### ⚠️ Documentation Files (Manual Update Needed)
The following documentation files still reference `12345`. When using these examples, replace `12345` with `meowdj@32`:

- **TESTING_GUIDE.md** - Multiple cURL examples
- **CURL_TESTS.md** - All test commands
- **API_KEY_GUIDE.md** - All examples and references

---

## Quick Reference for GUVI Submission

### For GUVI Official Tester:
**Headers:**
```
x-api-key: meowdj@32
```

**Endpoint:**
```
http://localhost:8000/webhook
```
(Or your deployed URL)

### For cURL Testing:
```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -H "x-api-key: meowdj@32" \
  -d '{"sessionId": "test-001", "message": {"sender": "scammer", "text": "Your account is blocked", "timestamp": "1770005528731"}, "conversationHistory": []}'
```

### For Python Testing:
```python
headers = {"x-api-key": "meowdj@32"}
response = requests.post("http://localhost:8000/webhook", json=payload, headers=headers)
```

### For PowerShell Testing:
```powershell
$headers = @{"x-api-key" = "meowdj@32"}
Invoke-RestMethod -Uri "http://localhost:8000/webhook" -Method Post -Headers $headers -Body $body
```

---

## Test Now

Run the quick test to verify the new API key works:

```bash
cd C:\guvihackfinal\guvihclhack26\DJ\guvihack-main\backend
python quick_test.py
```

Expected output should show successful authentication with the new key.

---

## For Your Submission Documentation

Include this in your README or submission notes:

```markdown
## API Authentication

**Endpoint:** POST /webhook

**Required Header:**
- `x-api-key: meowdj@32`

**Example Request:**
```bash
curl -X POST https://your-api-url.com/webhook \
  -H "Content-Type: application/json" \
  -H "x-api-key: meowdj@32" \
  -d '{
    "sessionId": "session-123",
    "message": {
      "sender": "scammer",
      "text": "Your account is suspended",
      "timestamp": "1770005528731"
    },
    "conversationHistory": []
  }'
```
\`\`\`

**Note:** The API key `meowdj@32` is required for all requests to the `/webhook` endpoint.
\`\`\`

---

## Security Note

Remember:
- ✅ `meowdj@32` = Your honeypot API key (share with evaluators)
- ✅ `GROQ_API_KEY` = Your Groq service key (keep private in `.env`)
- ✅ `LIVEKIT_API_KEY` = Your LiveKit key (keep private in `.env`)

Never commit your `.env` file to Git!
