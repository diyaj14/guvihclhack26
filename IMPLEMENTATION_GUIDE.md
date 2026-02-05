# Vigilante AI - Implementation Guide
**Agentic Honey-Pot for Scam Detection & Intelligence Extraction (Text & Voice)**

## 1. Executive Summary
"Vigilante AI" is a multi-modal Agentic system designed to trap scammers across **SMS/WhatsApp** and **Voice Calls**. It features a unified "Command Center" dashboard where an admin can monitor attacks and authorize the AI to "Take Over" conversations instantly.

## 2. Architecture: Two Modules, One Brain
The system is split into two active modules that feed into a central Intelligence Core.

### Module A: Text HoneyPot (FastAPI + "DJ" Enhanced Core)
*   **Input**: Webhooks from messaging platform (or Mock API).
*   **Hybrid Detection**:
    *   **Layer 1 (Fast)**: Regex/Keyword scan (Urgency, Fear, Payment keywords) for instant <100ms flagging.
    *   **Layer 2 (Smart)**: LLM verification if confidence is medium.
*   **Agent Core (Strategy Engine)**:
    *   **Dynamic Strategies**: Agent selects from "Playing Dumb", "Panic Trigger", "False Compliance" based on scammer aggression.
    *   **Persona**: "Ramesh Kumar" (45yo) or "Grandma" (70yo).
*   **Features**:
    *   **GUVI Callback**: Dedicated service to push `totalMessages`, `scamDetected`, `extractedIntelligence` to evaluation server.
    *   **Intelligence**: Regex patterns for UPI/IBAN extraction.

### Module B: Voice HoneyPot (LiveKit + Twilio)
*   **Input**: Telephony stream (SIP/WebSocket).
*   **Flow**:
    1.  **Twilio** receives call -> Streams audio to **LiveKit**.
    2.  **LiveKit Agent**:
        *   **Ear (STT)**: Deepgram (Instant transcription).
        *   **Brain (LLM)**: Groq (Llama 3) for sub-second responses.
        *   **Voice (TTS)**: Cartesia/ElevenLabs (Simulates elderly voice).
    3.  **Output**: Audio streamed back to scammer.
*   **Features**: Interruptibility (Barge-in), Filler words ("Umm..."), Background noise.

### Module C: Vigilante Dashboard (React)
*   **Unified View**: Tabs for "Live SMS" and "Active Calls".
*   **"Take Over" Button**: A big red button on the UI.
    *   *Auto Mode*: AI replies automatically using "Strategy Engine".
    *   *Manual Mode*: Human types/speaks, AI mimics the persona.
*   **Analytics**: "Money Saved", "Scammers Wasted", "Strategy Success Rate".

## 3. Tech Stack
*   **Frontend**: React, Tailwind CSS, Shadcn UI, Lucide React (Icons), LiveKit Client SDK.
*   **Backend**: Python, FastAPI.
    *   **Services**: `app/services/scam_detector.py`, `app/services/agent.py`, `app/services/intelligence_extractor.py`.
*   **Voice Pipeline**: LiveKit Agents Framework (Python).
*   **AI Services**: Groq (Llama 3.1), Deepgram (STT), Cartesia (TTS).

## 4. Implementation Workflow

### Phase 1: The Enhanced Backend (DJ Core)
1.  **Structure**: Create `app/services` structure.
2.  **Scam Detector**: Implement the "Weighted Keyword" logic.
3.  **Agent**: Implement the "Strategy Selector" (Random/Contextual choice).
4.  **Callback**: Implement `app/utils/callbacks.py` for mandatory GUVI integration.

### Phase 2: The Voice Module
1.  **LiveKit Setup**: Install `livekit-agents`.
2.  **Voice Agent Script**: Create `voice_agent.py` linked to the same "Strategy Engine".
3.  **Browser Demo**: "Browser Call" mode in dashboard.

### Phase 3: The Vigilante Dashboard
1.  **War Room UI**: Integate WebSocket stream.
2.  **Simulated Attack**: Button to trigger a "Bank Fraud" scenario.
3.  **Take Over**: Manual override controls.

## 5. Directory Structure
```
/root
  /backend
    /app
      main.py
      voice_agent.py
      /services
        scam_detector.py      # Hybrid (Keyword + LLM)
        agent.py              # Strategy Engine
        intelligence_extractor.py # Regex
        conversation_manager.py # Session State
      /utils
        callbacks.py          # GUVI Integration
  /frontend
    /src
      /components
      App.jsx
```

## 6. How to Win (Judge Impressions)
*   **Latency Demo**: Show the "Voice" tab. Talk fast. Show the AI keeping up.
*   **"The Button"**: During the demo, say "I'll let the AI handle this," press the button, and take your hands off the keyboard.
*   **Visuals**: Use a waveform that reacts to the AI's voice.
