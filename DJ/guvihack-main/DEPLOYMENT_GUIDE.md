# 🚀 Deployment Guide for Hackathon Submission

## Why Deploy?

The GUVI API tester needs a **public URL** to test your honeypot. `localhost` only works on your computer.

---

## Recommended: Deploy to Render (Free)

### Step 1: Prepare Your Code

1. **Make sure `.gitignore` excludes `.env`:**
   ```
   .env
   __pycache__/
   *.pyc
   ```

2. **Your `Procfile` should contain:**
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
   ✅ Already configured in your project!

3. **Your `requirements.txt` should list all dependencies:**
   ```
   fastapi
   uvicorn
   python-dotenv
   groq
   pydantic
   requests
   livekit-api
   ```
   ✅ Already configured!

### Step 2: Push to GitHub

```bash
cd C:\guvihackfinal\guvihclhack26\DJ\guvihack-main\backend
git init
git add .
git commit -m "Initial commit - Vigilante AI Honeypot"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/vigilante-ai.git
git push -u origin main
```

### Step 3: Deploy on Render

1. **Go to:** https://render.com
2. **Sign up** (use GitHub account for easy integration)
3. **Click "New +"** → **"Web Service"**
4. **Connect your GitHub repository**
5. **Configure:**
   - **Name:** `vigilante-ai-honeypot`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** `Free`

6. **Add Environment Variables:**
   Click "Advanced" → "Add Environment Variable"
   
   Add these:
   ```
   GROQ_API_KEY = your_groq_key_here
   LIVEKIT_API_KEY = your_livekit_key
   LIVEKIT_API_SECRET = your_livekit_secret
   LIVEKIT_URL = wss://vigilante-nk6tbkbt.livekit.cloud
   ```

7. **Click "Create Web Service"**

8. **Wait for deployment** (5-10 minutes)

9. **Copy your URL:** `https://vigilante-ai-honeypot.onrender.com`

### Step 4: Test Your Deployed API

**In GUVI Tester:**
- **Honeypot API Endpoint URL:** `https://vigilante-ai-honeypot.onrender.com/webhook`
- **x-api-key:** `meowdj@32`

**Or test with cURL:**
```bash
curl -X POST https://vigilante-ai-honeypot.onrender.com/webhook \
  -H "Content-Type: application/json" \
  -H "x-api-key: meowdj@32" \
  -d '{"sessionId": "test-001", "message": {"sender": "scammer", "text": "Your account is blocked", "timestamp": "1770005528731"}, "conversationHistory": []}'
```

---

## Alternative: Quick Testing with ngrok

If you need to test **right now** without deploying:

### Step 1: Download ngrok
- Go to https://ngrok.com/download
- Download and extract

### Step 2: Run ngrok
```bash
ngrok http 8000
```

### Step 3: Use the Public URL
Copy the `https://` URL from ngrok output (e.g., `https://abc123.ngrok.io`)

**In GUVI Tester:**
- **URL:** `https://abc123.ngrok.io/webhook`
- **x-api-key:** `meowdj@32`

⚠️ **Note:** ngrok URL changes each restart (free tier)

---

## Other Deployment Options

### Railway.app (Free Tier)
1. Go to https://railway.app
2. Connect GitHub repo
3. Add environment variables
4. Deploy

### Vercel (For Next.js frontend)
Your frontend can be deployed to Vercel:
```bash
cd C:\guvihackfinal\guvihclhack26\DJ\guvihack-main\frontend
vercel
```

### Heroku (Paid)
Heroku removed free tier, but if you have credits:
```bash
heroku create vigilante-ai
git push heroku main
heroku config:set GROQ_API_KEY=your_key
```

---

## Troubleshooting Deployment

### Issue: "Module not found"
**Fix:** Make sure all dependencies are in `requirements.txt`

### Issue: "Port already in use"
**Fix:** Render/Railway automatically set `$PORT`. Use:
```python
port = int(os.getenv("PORT", 8000))
uvicorn.run(app, host="0.0.0.0", port=port)
```

### Issue: "Environment variables not found"
**Fix:** Add them in the Render/Railway dashboard under "Environment"

### Issue: "Connection timeout"
**Fix:** 
- Check if service is running (Render dashboard shows logs)
- Verify URL is correct (no trailing slash before `/webhook`)
- Make sure firewall allows outbound connections

---

## For Final Submission

**Document your deployed URL:**

```markdown
## Live Demo

**API Endpoint:** https://vigilante-ai-honeypot.onrender.com/webhook

**Authentication:** 
- Header: `x-api-key: meowdj@32`

**Test with:**
```bash
curl -X POST https://vigilante-ai-honeypot.onrender.com/webhook \
  -H "Content-Type: application/json" \
  -H "x-api-key: meowdj@32" \
  -d '{"sessionId": "demo", "message": {"sender": "scammer", "text": "Your account is suspended", "timestamp": "1770005528731"}, "conversationHistory": []}'
```

**Frontend:** https://your-frontend.vercel.app
**Voice Agent:** Running on LiveKit Cloud
\`\`\`
```

---

## Recommended Approach

1. **For immediate testing:** Use ngrok (5 minutes setup)
2. **For submission:** Deploy to Render (free, permanent URL)
3. **For frontend:** Deploy to Vercel (free, fast)

This ensures GUVI evaluators can test your API without any local setup! 🚀
