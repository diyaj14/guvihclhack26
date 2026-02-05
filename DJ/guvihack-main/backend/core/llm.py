import os
import re
import json
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path
from .prompts import Persona

# Robstly load .env from the backend directory
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Fallback: try loading from CWD if specific path fails or just to be safe
load_dotenv()

MSG_HISTORY = []


class VigilanteBrain:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY", "gsk_placeholder"))
        
    def generate_response(self, user_input: str, persona: Persona, conversation_history: list = None, extracted_intel: dict = None):
        """
        Generates a response with intelligence extraction focus and dynamic context
        """
        
        # Build conversation context
        context = ""
        if conversation_history:
            context = "\n\nCONVERSATION SO FAR:\n"
            # Show last 10 messages for better flow awareness
            for msg in conversation_history[-10:]:
                if isinstance(msg, dict):
                    text = msg.get('text') or msg.get('content') or ""
                    sender_raw = msg.get('sender') or msg.get('role') or "user"
                else:
                    text = getattr(msg, 'text', getattr(msg, 'content', ''))
                    sender_raw = getattr(msg, 'sender', getattr(msg, 'role', 'user'))
                
                label = "YOU" if sender_raw in ['user', 'assistant'] else "SCAMMER"
                context += f"{label}: {text}\n"
        
        # Determine status based on intelligence gathered
        intel_count = sum(len(v) for v in extracted_intel.values()) if extracted_intel else 0
        current_phase = "ENGAGEMENT" if intel_count == 0 else "EXTRACTION"
        
        system_msg = f"""
{persona.system_prompt}

🚨 TONE & FLOW CONSTRAINTS:
- BE NATURAL. Respond directly to the Scammer's last message.
- SUB 12 WORDS per message. No filler like "Oh hello".
- NEVER repeat the same strategy or "tech error" twice. Use variety.
- If they have already said their name (see INTEL GATHERED), DO NOT ask "who's this?" or "what's ur name?".
- If they ask a question, answer it in character before moving to your goal.

🚨 SESSION STATE:
- CURRENT PHASE: {current_phase}
- INTEL GATHERED SO FAR: {json.dumps(extracted_intel or {})}
- GOAL: Extract {', '.join(persona.intelligence_targets)} without being suspicious.

{context}

🤖 LATEST SCAMMER MESSAGE: "{user_input}"

IMPORTANT: You must respond in valid JSON format ONLY.
{{
    "analysis": "Short analysis of their intent",
    "strategy": "Your current tactic (e.g. 'faking error', 'distracting', 'verifying ID')",
    "reply": "Your in-character response (short, lowercase, informal)",
    "extractedIntel": {{
        "scammerName": [], "bankAccounts": [], "upiIds": [], "phishingLinks": [], "phoneNumbers": [],
        "jobTitle": [], "companyNames": [], "location": [], "suspiciousKeywords": []
    }}
}}
"""
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_input}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=1000,
                response_format={"type": "json_object"}
            )
            
            response_text = chat_completion.choices[0].message.content
            
            # Parse and validate
            return response_text
            
        except Exception as e:
            print(f"LLM Error: {str(e)}")
            # Fallback JSON
            return json.dumps({
                "analysis": "Error occurred",
                "extractionTarget": "none",
                "strategy": "Error recovery",
                "reply": "sorry wait... my phone is glitching. what did u say?",
                "extractedIntel": {}
            })

    def extract_intelligence_from_text(self, text: str) -> dict:
        """
        Fallback regex-based intelligence extraction
        Use this in addition to LLM extraction for redundancy
        """
        intel = {
            "scammerName": [],
            "bankAccounts": [],
            "upiIds": [],
            "phishingLinks": [],
            "phoneNumbers": [],
            "jobTitle": [],
            "companyNames": [],
            "location": [],
            "suspiciousKeywords": []
        }
        
        # Name Extraction (myself [Name], I am [Name], etc.)
        name_match = re.search(r'(?:myself|i am|this is|i\'m)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', text, re.IGNORECASE)
        if name_match:
            intel["scammerName"].append(name_match.group(1).strip())
        
        # Bank account patterns (Indian format - usually 11+ digits to avoid phone collision)
        bank_patterns = [
            r'\b\d{11,18}\b',  # 11-18 digit account numbers
            r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'  # Formatted (16 digits)
        ]
        for pattern in bank_patterns:
            matches = re.findall(pattern, text)
            intel["bankAccounts"].extend(matches)
        
        # UPI IDs
        upi_pattern = r'\b[\w\.\-]+@[\w]+\b'
        intel["upiIds"] = re.findall(upi_pattern, text)
        
        # Phone numbers (Indian format)
        phone_patterns = [
            r'\+91[-\s]?\d{10}',
            r'\b[6-9]\d{9}\b',
            r'\b\d{3}[-\s]\d{3}[-\s]\d{4}\b'
        ]
        for pattern in phone_patterns:
            matches = re.findall(pattern, text)
            intel["phoneNumbers"].extend(matches)
        
        # URLs/Links
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        intel["phishingLinks"] = re.findall(url_pattern, text)
        
        job_keywords = ['manager', 'officer', 'department', 'division', 'supervisor', 'agent', 'support']
        for word in job_keywords:
            if word in text.lower():
                # Extract only a few words around the keyword, but STOP at prepositions
                # This prevents "branch manager at new delhi" from being one block
                match = re.search(fr'((?:\w+\W+){{0,2}}\b{word}\b)', text, re.IGNORECASE)
                if match:
                    clean_job = match.group(1).strip().lower()
                    # Remove "i am", "myself", "this is"
                    clean_job = re.sub(r'^(i am|myself|this is|is|am|a)\s+', '', clean_job)
                    intel["jobTitle"].append(clean_job.title())
        
        # Location Extraction (Indian Cities & General Keywords)
        cities = ['Delhi', 'Mumbai', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad', 'Gurgaon', 'Noida']
        city_pattern = fr"\b(?:{'|'.join(cities)})\b"
        intel["location"] = re.findall(city_pattern, text, re.IGNORECASE)
        # Also check for "at [Place]" or "from [Place]"
        place_match = re.search(r'(?:at|from|in)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', text)
        if place_match:
            intel["location"].append(place_match.group(1).strip())

        # Suspicious keywords
        keywords = [
            'urgent', 'verify', 'suspended', 'blocked', 'immediately',
            'account', 'security', 'update', 'confirm', 'expire',
            'risk', 'unauthorized', 'unusual activity', 'click here',
            'limited time', 'act now', 'verify now', 'customer care',
            'prize', 'winner', 'congratulations', 'refund', 'KYC'
        ]
        found_keywords = [kw for kw in keywords if kw.lower() in text.lower()]
        intel["suspiciousKeywords"] = found_keywords
        
        # Remove duplicates and substring overlaps
        for key in intel:
            items = list(set(intel[key]))
            items.sort(key=len, reverse=True)
            unique_items = []
            for item in items:
                if not any(item.lower() in u.lower() for u in unique_items):
                    unique_items.append(item)
            intel[key] = unique_items

        # Deduplicate Names from Job Titles
        # If a job title contains a name that was extracted, clean the job title
        names = intel.get("scammerName", [])
        if names:
            cleaned_jobs = []
            for job in intel["jobTitle"]:
                cleaned_job = job
                for name in names:
                    # Case insensitive removal of name from job title
                    cleaned_job = re.sub(rf'\b{re.escape(name)}\b', '', cleaned_job, flags=re.IGNORECASE).strip(' ,')
                if cleaned_job:
                    cleaned_jobs.append(cleaned_job)
            intel["jobTitle"] = cleaned_jobs
        
        return intel
