# Using ngrok to Expose Local API

## What is ngrok?
ngrok creates a secure tunnel from a public URL to your local server, allowing GUVI to test your local API.

## Steps:

### 1. Download ngrok
- Go to https://ngrok.com/download
- Download for Windows
- Extract the zip file

### 2. Run ngrok
Open a new terminal and run:
```bash
ngrok http 8000
```

### 3. Copy the Public URL
You'll see output like:
```
Forwarding    https://abc123.ngrok.io -> http://localhost:8000
```

### 4. Use in GUVI Tester
**Honeypot API Endpoint URL:**
```
https://abc123.ngrok.io/webhook
```

**Headers:**
```
x-api-key: meowdj@32
```

### 5. Test
Click "Test Honeypot Endpoint" in GUVI's tester.

## Important Notes:
- ⚠️ Keep ngrok running while testing
- ⚠️ The URL changes each time you restart ngrok (free tier)
- ⚠️ Free tier has request limits
- ✅ Perfect for quick testing before deployment

## Alternative: ngrok with Auth Token (Recommended)
1. Sign up at https://ngrok.com
2. Get your auth token
3. Run: `ngrok authtoken YOUR_AUTH_TOKEN`
4. Then: `ngrok http 8000`

This gives you:
- Persistent URLs
- Higher limits
- Better reliability
