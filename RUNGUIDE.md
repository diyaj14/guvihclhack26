# 🚀 Vigilante AI - Comprehensive Run Guide

Welcome to **Vigilante AI**, the next-generation "HoneyPot" system designed to intercept and engage scammers using advanced Agentic AI. This guide will help you set up and run the **Voice Agentic Suite**.

---

## 🏗️ Project Architecture
The current implementation focuses on the **Voice Module (Phase 3)**, featuring:
- **Autonomous Brain**: Python-based LiveKit agent with sub-second latency.
- **Dynamic Personas**: Simulated characters (Mrs. Sharma, Ramesh, etc.) to deceive scammers.
- **Multimodal UI**: Two premium, interactive frontend variants with audio reactivity.

---

## ⚡ Quick Start

### 1. Prerequisites
- **Python 3.10+** (Recommend 3.12)
- **LiveKit Account**: Get keys from [livekit.io](https://livekit.io)
- **Deepgram Account**: Get keys from [deepgram.com](https://deepgram.com)
- **Groq Account**: Get keys from [groq.com](https://groq.com)

### 2. Environment Setup
Navigate to the voice module and configure your API keys.

```powershell
cd Phase3_Voice
# Open .env and fill in your keys:
# LIVEKIT_URL=wss://...
# LIVEKIT_API_KEY=...
# LIVEKIT_API_SECRET=...
# DEEPGRAM_API_KEY=...
# GROQ_API_KEY=...
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Authenticate the Frontend
You must generate a fresh JWT token to allow the browser to connect to your LiveKit room.

```powershell
python generate_token.py
```
> [!IMPORTANT]
> Copy the generated token and paste it into `frontend_demo/index.html` (or `index2.html`) inside the `const TOKEN = "..."` variable.

---

## 🎙️ Running the Agentic Suite

### Step 1: Start the AI Brain
Launch the agent in development mode. This agent listens for incoming participants in the LiveKit room.

```powershell
python agent/agent.py dev
```

### Step 2: Open the Intercept Dashboard
Open one of the UI variants in your browser (recommend Chrome or Edge).

| Variant | Filename | Aesthetic |
| :--- | :--- | :--- |
| **PULSE** | `index.html` | Antigravity particles with audio-reactive bursts. |
| **LIQUID** | `index2.html` | Gourmet liquid blob that flows with your cursor. |

1. Open the file directly (e.g., `Phase3_Voice/frontend_demo/index.html`).
2. Select a **Persona** from the dropdown (e.g., "Mrs. Sharma").
3. Click **"Connect Neural Link"**.
4. **Speak!** The AI will detect your voice and respond in-character.

---

## 🧪 Testing Scenarios
Try these interactions to see the Agent in action:

- **The Bank Scam**: Say "Hello, I am calling from your bank regarding unauthorized transactions."
- **The Lottery**: Say "Congratulations! You have won 1 Crore in the national lottery."
- **Verification**: Say "Can you please verify your Aadhaar or PAN number?"

Observe how the AI (e.g., Mrs. Sharma) acts confused, plays along, or provides fake "intelligence" to waste the scammer's time.

---

## 🛠️ Components Reference

### `Phase3_Voice/agent/agent.py`
The core logic. It manages the connection between the Voice Pipeline (STT -> LLM -> TTS) and handles the "entrypoint" when a scammer joins.

### `Phase3_Voice/agent/personas.py`
Contains the detailed "System Prompts" for each character. Edit this to change how the AI behaves.

### `Phase3_Voice/generate_token.py`
A utility to create short-lived access tokens for the frontend.

---

## 🚨 Troubleshooting
- **Link Error**: Ensure `agent.py` is running and the `TOKEN` in your HTML is fresh.
- **Microphone Issues**: Ensure you have allowed microphone permissions in your browser.
- **Latency**: If the AI is slow, check your internet connection or verify your Groq/Deepgram API limits.

---
*Created for the GUVI HCL Hackathon '26*
