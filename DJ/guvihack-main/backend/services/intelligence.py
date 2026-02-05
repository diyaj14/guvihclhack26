import re
from pydantic import BaseModel

class ExtractedIntelligence(BaseModel):
    scammer_name: list[str] = []
    upi_ids: list[str] = []
    phone_numbers: list[str] = []
    urls: list[str] = []
    bank_details: list[str] = []

class IntelligenceExtractor:
    def _normalize_voice_text(self, text: str) -> str:
        """
        Converts spoken artifacts (number words, 'at') into digital formats.
        """
        text = text.lower()
        
        # Word-to-Digit mapping
        num_map = {
            'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4',
            'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9'
        }
        for word, digit in num_map.items():
            text = text.replace(word, digit)
            
        # Common voice replacements
        text = text.replace(" at ", "@").replace(" dot ", ".")
        return text

    def extract(self, text: str) -> ExtractedIntelligence:
        intel = ExtractedIntelligence()
        
        # 0. Normalize text for technical extraction (keep original for context/names)
        norm_text = self._normalize_voice_text(text)
        
        # 1. Names (Context-based)
        # Looks for "my name is X", "this is X calling"
        name_patterns = [
            r"my name is\s+([a-zA-Z]+)",
            r"this is\s+([a-zA-Z]+)\s+calling",
            r"speaking with\s+([a-zA-Z]+)"
        ]
        for pat in name_patterns:
            matches = re.findall(pat, text, re.IGNORECASE)
            for m in matches:
                if m.lower() not in ['scam', 'support', 'bank', 'manager']: # Filter noise
                    intel.scammer_name.append(m.title())
        
        # 2. UPI IDs (Targeting normalized text)
        # Matches: name@bank, name@upi, 1234@paytm
        intel.upi_ids = re.findall(r'[a-zA-Z0-9.\-_]+@[a-zA-Z0-9]+', norm_text)
        
        # 3. Phone Numbers
        # Matches: +91 987 654 3210, 9876543210, 9 8 7 6 5 4 3 2 1 0
        phone_matches = re.findall(r'(\+?\d(?:\s*[\-\.]?\s*\d){9,})', norm_text)
        for m in phone_matches:
            # Clean up: remove spaces/dots/dashes
            digits = re.sub(r'[\s\-\.]', '', m)
            if 10 <= len(digits) <= 15:
                intel.phone_numbers.append(digits)
        
        # 4. URLs
        intel.urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
        
        # 5. Bank Context
        keywords = ["account number", "ifsc", "routing number", "iban"]
        if any(k in text.lower() for k in keywords):
            intel.bank_details.append("Bank context detected")

        return intel

    def detect_scam(self, text: str) -> dict:
        """
        Analyzes message for scam intent using keywords and patterns.
        """
        score = 0
        reasons = []
        text_lower = text.lower()
        
        # 1. Urgency & Threats
        urgency_keywords = ['urgent', 'immediately', 'suspended', 'blocked', 'arrest', 'warrant', 'expire', 'lapse']
        if any(w in text_lower for w in urgency_keywords):
            score += 0.4
            reasons.append("Urgency/Threat detected")
            
        # 2. Financial Requests
        money_keywords = ['pay', 'transfer', 'upi', 'bank', 'refund', 'gpay', 'paytm', 'credit card', 'kyc']
        if any(w in text_lower for w in money_keywords):
            score += 0.3
            reasons.append("Financial request detected")
            
        # 3. Suspicious Links/Actions
        action_keywords = ['click here', 'link', 'download', 'apk', 'form']
        if any(w in text_lower for w in action_keywords):
            score += 0.3
            reasons.append("Suspicious action requested")
            
        # 4. Pattern Matching (Links/Phones)
        if re.search(r'http[s]?://', text):
            score += 0.2
            reasons.append("Contains URL")
            
        is_scam = score >= 0.4
        
        return {
            "is_scam": is_scam,
            "confidence": min(score, 1.0),
            "reasons": reasons
        }
