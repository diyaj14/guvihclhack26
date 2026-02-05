import requests
import json
import time

url = "http://localhost:8000/webhook"
session_id = f"test_session_{int(time.time())}"

def chat(message, history):
    payload = {
        "sessionId": session_id,
        "message": {"sender": "scammer", "text": message},
        "conversationHistory": history
    }
    headers = {"x-api-key": "12345"}
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

history = []

# Scenario: Scammer tries to give a bank ID and then a link
scenarios = [
    "hi",
    "how are u mam",
    "myself Vinod , general manager of state bank of india , delhi branch",
    "I need your ID to unblock. It's SBI-9922.",
    "Okay, now click this link to verify: http://sbi-verify-secure.com"
]

print(f"Starting Verification Session: {session_id}\n")

for msg in scenarios:
    print(f"\n[TURN {scenarios.index(msg) + 1}]")
    print(f"SCAMMER: {msg}")
    result = chat(msg, history)
    reply = result['reply']
    thought = result['debug_thought']
    intel = result['intelligence']
    
    print(f"BOT REPLY: {reply}")
    print(f"BOT THOUGHT: {thought}")
    print(f"EXTRACTED INTEL: {json.dumps(intel, indent=2)}")
    print("-" * 50)
    
    # Update history for next turn
    history.append({"sender": "scammer", "text": msg})
    history.append({"sender": "user", "text": reply})
    time.sleep(1) # Wait a bit between turns
