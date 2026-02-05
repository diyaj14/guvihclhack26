# ⚡ 4-DAY SPRINT CHEAT SHEET

**Print this. Post on wall. Follow exactly.**

---

## 📋 DAY 1: FOUNDATION (8 HOURS)

### Hour 1-2: Setup
```bash
mkdir scam-honeypot && cd scam-honeypot
python -m venv venv && source venv/bin/activate
mkdir -p app/{services,utils} && pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Hour 2-4: Copy Codebase
- Copy FILE 1 (main.py) from READY_TO_USE_CODEBASE.md
- Copy FILE 2 (scam_detector.py) 
- Copy FILE 7 (requirements.txt)
- Copy FILE 8 (.env with your API key)

### Hour 4-6: Create Services
- Copy FILE 2 → app/services/scam_detector.py
- Copy FILE 3 → app/services/agent.py
- Copy FILE 4 → app/services/intelligence_extractor.py
- Copy FILE 5 → app/services/conversation_manager.py
- Copy FILE 6 → app/utils/callbacks.py

### Hour 6-8: Test API
```bash
uvicorn app.main:app --reload
# In another terminal:
curl http://localhost:8000/health
```

### ✅ Day 1 Done?
- [ ] API running on localhost:8000
- [ ] Health check returns 200
- [ ] Can see API docs at localhost:8000/docs
- [ ] Code compiles without errors

---

## 🚀 DAY 2: TEST & AGENT (16 HOURS)

### Testing Phase (Hours 1-4)
Test analyze endpoint:
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "x-api-key: sk_test_123456789" \
  -H "Content-Type: application/json" \
  -d '{
    "message": {"sender": "scammer", "text": "Your account blocked. Verify immediately.", "timestamp": "2026-01-31T10:00:00Z"},
    "metadata": {"channel": "SMS", "language": "English"}
  }'
```

Expected response:
```json
{
  "status": "success",
  "sessionId": "some-uuid",
  "is_scam": true,
  "confidence": 0.85,
  "severity": "high",
  "scam_type": "bank_fraud",
  "explanation": "Urgency tactics..."
}
```

Test with 5+ real scam messages. Accuracy should be >80%

### Agent Integration (Hours 4-8)
Verify agent is imported in main.py. Test engage endpoint:
```bash
curl -X POST http://localhost:8000/api/engage \
  -H "x-api-key: sk_test_123456789" \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "YOUR_SESSION_ID_FROM_ANALYZE",
    "message": {"sender": "scammer", "text": "Share your UPI", "timestamp": "2026-01-31T10:01:00Z"},
    "conversationHistory": [{"sender": "scammer", "text": "Your account blocked...", "timestamp": "2026-01-31T10:00:00Z"}],
    "metadata": {"channel": "SMS"}
  }'
```

Expected: Natural, believable response

### Multi-turn Testing (Hours 8-12)
```
Message 1: "Your account blocked"
  → Your response: "Oh no! What do I do?"

Message 2: "Click here to verify"
  → Your response: "I'm scared. Can you explain?"

Message 3: "Share your UPI ID"
  → Your response: "But how do I know it's real?"
```

Test until agent responses feel natural.

### Intelligence Extraction (Hours 12-16)
Test that UPI/phone/links are extracted:
```
Input: "Transfer to scammer@upi immediately or +919876543210"
Output should include:
- upiIds: ["scammer@upi"]
- phoneNumbers: ["+919876543210"]
```

### ✅ Day 2 Done?
- [ ] Detection accuracy >85% (test with 10 messages)
- [ ] Agent generates 5+ different response types
- [ ] Agent responses don't repeat same template
- [ ] Intelligence extraction works (UPI, phones, links)
- [ ] Session persistence working

---

## 💬 DAY 3: CALLBACK & POLISH (16 HOURS)

### GUVI Callback (Hours 1-4) - CRITICAL!
Verify FILE 6 (callbacks.py) is:
- [ ] In app/utils/callbacks.py
- [ ] Imported in main.py
- [ ] Async function
- [ ] Sending to correct URL

Test callback manually:
```bash
# After running engage endpoint multiple times
curl -X POST http://localhost:8000/api/finalize-session/YOUR_SESSION_ID \
  -H "x-api-key: sk_test_123456789"
```

Should return:
```json
{
  "status": "success",
  "message": "Intelligence sent to GUVI"
}
```

### Accuracy Tuning (Hours 4-8)
If accuracy <85%, adjust scam_detector.py:
```python
# Increase urgency + fear boost if missing true positives
if urgency_present and fear_present:
    threat += 0.20  # Was 0.15, increased
```

Test again with same 10 messages. Target: >85%

### Response Format Validation (Hours 8-12)
Check every response matches spec:
```
/api/analyze returns:
{
  "status": "success",
  "sessionId": string,
  "is_scam": boolean,
  "confidence": 0-1,
  "severity": "high|medium|low",
  "scam_type": string,
  "explanation": string
}

/api/engage returns:
{
  "status": "success",
  "sessionId": string,
  "reply": string,
  "intelligence_extracted": object,
  "session_status": "ongoing|complete"
}
```

### Final Testing (Hours 12-16)
Test complete conversation:
1. Analyze (detect scam)
2. Engage x5 (multi-turn)
3. Get intelligence
4. Finalize (send callback)

All 4 steps should work perfectly.

### ✅ Day 3 Done?
- [ ] GUVI callback working (HTTP 200-201)
- [ ] Detection accuracy >85%
- [ ] Agent responses natural
- [ ] Intelligence extraction >95% accurate
- [ ] Response format 100% correct
- [ ] Tested complete workflow

---

## 🌐 DAY 4: DEPLOY & SUBMIT (8 HOURS)

### Deploy to Hugging Face Spaces (Hour 1)
```bash
git init
git add .
git commit -m "Initial: Agentic Honeypot"

# Create space at huggingface.co/spaces
# Name: scam-honeypot
# SDK: Docker

git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/scam-honeypot
git push hf main

# Wait 2-3 minutes for deployment
# Your API: https://YOUR_USERNAME-scam-honeypot.hf.space
```

### Test Deployed API (Hour 2)
```bash
# Replace with your deployed URL
URL="https://YOUR_USERNAME-scam-honeypot.hf.space"

# Health check
curl $URL/health

# Test analyze
curl -X POST $URL/api/analyze \
  -H "x-api-key: sk_test_123456789" \
  -H "Content-Type: application/json" \
  -d '{"message": {"sender": "scammer", "text": "Your account blocked. Verify immediately.", "timestamp": "2026-01-31T10:00:00Z"}, "metadata": {"channel": "SMS", "language": "English"}}'

# If it works, continue!
```

### Documentation (Hour 3)
Update README.md:
```markdown
# Agentic Honeypot - Scam Detection API

API: https://YOUR_USERNAME-scam-honeypot.hf.space

## Features
- Real-time scam detection (>85% accuracy)
- Autonomous AI agent engagement
- Multi-turn conversations
- Intelligence extraction
- GUVI integration

## Quick Test
[Include your curl commands above]
```

### Final Verification (Hour 4)
Checklist before submission:
- [ ] API deployed and accessible
- [ ] All endpoints working on cloud
- [ ] GUVI callback functional
- [ ] Health check returns 200
- [ ] Documentation complete
- [ ] Can test with curl commands

### Last-Minute Backup (Hour 5-8)
If deployment fails:
1. Push code to GitHub with README
2. Include setup instructions for local testing
3. Include curl commands for testing
4. Document everything

## ✅ Day 4 Done?
- [ ] API live on cloud
- [ ] Permanent URL accessible
- [ ] All endpoints tested
- [ ] Callback working
- [ ] Documentation complete
- [ ] Ready to submit

---

## 🎯 SUBMISSION CHECKLIST

**Before submitting**, verify:

### Functionality ✅
- [ ] POST /api/analyze - Works
- [ ] POST /api/engage - Works  
- [ ] GET /api/session/{id}/intelligence - Works
- [ ] GUVI callback - Sends successfully
- [ ] API key validation - Working

### Format ✅
- [ ] JSON responses valid
- [ ] All required fields present
- [ ] confidence: float 0-1
- [ ] severity: string (high|medium|low)
- [ ] scam_type: string
- [ ] explanation: string

### Testing ✅
- [ ] Tested with 5+ scam messages
- [ ] Tested multi-turn conversation
- [ ] Tested legitimate messages (false positives <5%)
- [ ] Tested GUVI callback
- [ ] Response time <2 seconds

### Deployment ✅
- [ ] Live on cloud (HF Spaces/Render)
- [ ] Has permanent URL
- [ ] Can test with curl
- [ ] Documentation complete

---

## 🚨 CRITICAL THINGS NOT TO FORGET

1. **GUVI CALLBACK** - Most teams will forget this
   - Must send: sessionId, scamDetected, totalMessages, extractedIntelligence, agentNotes
   - Must POST to: https://hackathon.guvi.in/api/updateHoneyPotFinalResult
   - This is mandatory for scoring!

2. **API KEY VALIDATION** - Verify x-api-key header
   - If missing: return 401
   - If invalid: return 403

3. **RESPONSE FORMAT** - Must be JSON with exact fields
   - Missing fields = points deducted
   - Wrong format = API call fails

4. **ACCURACY** - Target >85%
   - Test with real scam messages
   - Adjust keyword weights if needed
   - Test multi-turn conversations

---

## ⏰ TIME TRACKER

| Task | Planned | Actual | Status |
|------|---------|--------|--------|
| Setup | 2h | __ | |
| Codebase copy | 2h | __ | |
| Testing | 4h | __ | |
| Integration | 4h | __ | |
| Callback | 2h | __ | |
| Accuracy tuning | 4h | __ | |
| Deployment | 2h | __ | |
| Final testing | 2h | __ | |

**Total: ~24 hours across 4 days** (6h/day average)

---

## 💡 IF THINGS GO WRONG

**API not running?**
- Check ANTHROPIC_API_KEY in .env
- Check port 8000 not in use
- Run: `python -m spacy download en_core_web_sm`

**Agent responses robotic?**
- Increase temperature in agent.py (0.9+)
- Add more emotion keywords
- Use varied prompt strategies

**Callback failing?**
- Check JSON format
- Verify all fields present
- Test with: curl -X POST https://hackathon.guvi.in/api/updateHoneyPotFinalResult

**Deployment failing?**
- Check requirements.txt complete
- Verify ANTHROPIC_API_KEY set as environment variable
- HF Spaces: Set in Space settings
- Render: Set in Config Variables

---

## 🏆 REMEMBER

You have **everything you need** to win.

Follow this plan exactly.
Don't add extra features (scope creep kills projects).
Test constantly.
Deploy early.

**You've got this!** 🚀

---

**Print this cheat sheet. Follow it. Win.**

*Last Updated: January 31, 2026 | Final 4-Day Edition*
