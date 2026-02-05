import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
print(f"API Key found: {api_key[:5]}...{api_key[-5:] if api_key else 'None'}")

if not api_key:
    # Fallback to hardcoded key if env load fails (just for test)
    api_key = "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"

try:
    client = Groq(api_key=api_key)
    print("Connecting to Groq...")
    
    completion = client.chat.completions.create(
        messages=[{"role": "user", "content": "ping"}],
        model="llama-3.3-70b-versatile", 
    )
    
    print("Success!")
    print(completion.choices[0].message.content)

except Exception as e:
    print(f"FAILED: {e}")
