# 🔑 API Key Configuration Guide

## Understanding the API Key

The `x-api-key` header is used to authenticate requests to your Vigilante AI API. This prevents unauthorized access to your honeypot system.

---

## Current Configuration

**Location:** `backend/main.py` (Lines 118-122)

```python
@app.post("/webhook", response_model=AgentAPIResponse)
async def scam_webhook(
    data: ChallengeInput, 
    background_tasks: BackgroundTasks,
    x_api_key: str = Header(None)
):
    # Auth Check
    if x_api_key != "YOUR_SECRET_API_KEY" and x_api_key != "12345": 
        raise HTTPException(status_code=401, detail="Invalid API Key")
```

**Currently Accepted Keys:**
- `12345` - Simple test key (for local development)
- `YOUR_SECRET_API_KEY` - Placeholder (should be replaced)

---

## For Testing (Local Development)

**Use the test key:** `12345`

### Example cURL:
```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -H "x-api-key: 12345" \
  -d '{"sessionId": "test-001", "message": {"sender": "scammer", "text": "Test", "timestamp": "1770005528731"}, "conversationHistory": []}'
```

### Example Python:
```python
headers = {"x-api-key": "12345"}
response = requests.post("http://localhost:8000/webhook", json=payload, headers=headers)
```

---

## For Production/Hackathon Submission

### Option 1: Use Environment Variable (Recommended)

1. **Add to `.env` file:**
   ```env
   API_SECRET_KEY=your-strong-secret-key-here-abc123xyz
   ```

2. **Update `main.py`:**
   ```python
   import os
   from dotenv import load_dotenv
   
   load_dotenv()
   VALID_API_KEY = os.getenv("API_SECRET_KEY", "12345")
   
   @app.post("/webhook", response_model=AgentAPIResponse)
   async def scam_webhook(
       data: ChallengeInput, 
       background_tasks: BackgroundTasks,
       x_api_key: str = Header(None)
   ):
       if x_api_key != VALID_API_KEY:
           raise HTTPException(status_code=401, detail="Invalid API Key")
   ```

3. **Generate a strong key:**
   ```python
   import secrets
   print(secrets.token_urlsafe(32))
   # Example output: "xK7mP9nQ2wR5tY8uI1oP4aS6dF3gH0jK9lZ2xC5vB7nM"
   ```

### Option 2: Keep Simple Key for Hackathon

If GUVI evaluators need to test your API, you can:

1. **Keep the simple key:** `12345`
2. **Or choose a memorable key:** `guvi-hackathon-2026`
3. **Update `main.py`:**
   ```python
   if x_api_key != "guvi-hackathon-2026":
       raise HTTPException(status_code=401, detail="Invalid API Key")
   ```
4. **Share this key with evaluators** in your submission documentation

---

## For GUVI's Official Tester

When using GUVI's API endpoint tester (the form you showed):

**Headers:**
```
x-api-key: 12345
```

**Honeypot API Endpoint URL:**
```
http://localhost:8000/webhook
```
(Or your deployed URL if hosted online)

---

## Testing Authentication

### Test 1: Valid Key (Should succeed)
```bash
curl -X POST http://localhost:8000/webhook \
  -H "x-api-key: 12345" \
  -H "Content-Type: application/json" \
  -d '{"sessionId": "auth-test", "message": {"sender": "scammer", "text": "Test", "timestamp": "1770005528731"}, "conversationHistory": []}'
```

**Expected:** Status 200, JSON response with agent reply

### Test 2: Invalid Key (Should fail)
```bash
curl -X POST http://localhost:8000/webhook \
  -H "x-api-key: wrong-key" \
  -H "Content-Type: application/json" \
  -d '{"sessionId": "auth-test", "message": {"sender": "scammer", "text": "Test", "timestamp": "1770005528731"}, "conversationHistory": []}'
```

**Expected:** Status 401, `{"detail": "Invalid API Key"}`

### Test 3: Missing Key (Should fail)
```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{"sessionId": "auth-test", "message": {"sender": "scammer", "text": "Test", "timestamp": "1770005528731"}, "conversationHistory": []}'
```

**Expected:** Status 401, `{"detail": "Invalid API Key"}`

---

## Recommended Setup for Hackathon

### Keep it simple:

1. **Use `12345` for testing**
2. **Document it clearly** in your README/submission
3. **Tell evaluators:** "Use API key `12345` to test the endpoint"

### Or generate a custom key:

1. **Choose a key:** `guvi-vigilante-ai-2026`
2. **Update `main.py` line 121:**
   ```python
   if x_api_key != "guvi-vigilante-ai-2026":
   ```
3. **Document it:** "Use API key `guvi-vigilante-ai-2026`"

---

## Security Note

⚠️ **For a production system**, you should:
- Use strong, randomly generated keys
- Store keys in environment variables (`.env`)
- Never commit keys to Git
- Rotate keys regularly
- Use different keys for different environments (dev/staging/prod)

✅ **For this hackathon**, a simple memorable key is fine since:
- It's a demo/evaluation environment
- Evaluators need easy access
- The system will be decommissioned after evaluation

---

## Current Recommendation

**Keep using `12345` for now.** It's already configured and working. When you submit to GUVI, just document:

> **API Authentication:**  
> Use header `x-api-key: 12345` to authenticate requests to the `/webhook` endpoint.

This makes it easy for evaluators to test your system without confusion.

---

## Quick Reference

| Scenario | API Key to Use |
|----------|---------------|
| Local testing | `12345` |
| Python test scripts | `12345` (already configured) |
| GUVI official tester | `12345` |
| cURL commands | `12345` |
| Production deployment | Generate strong key with `secrets.token_urlsafe(32)` |

---

**Bottom Line:** You don't need to "get" an API key from anywhere. You **set** it yourself in your code, and then you **share** it with anyone who needs to test your API (like GUVI evaluators).
