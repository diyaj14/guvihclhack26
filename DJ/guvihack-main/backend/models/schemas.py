from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Union

class MessageObj(BaseModel):
    model_config = ConfigDict(
        extra='allow',  # Allow extra fields from hackathon tester
        str_strip_whitespace=True
    )
    
    sender: str
    text: str
    timestamp: Optional[Union[int, str]] = None  # Accept both int and string for compatibility

class MetadataObj(BaseModel):
    model_config = ConfigDict(extra='allow')  # Allow extra fields
    
    channel: str = "SMS"
    language: str = "English"
    locale: str = "IN"

class ChallengeInput(BaseModel):
    model_config = ConfigDict(
        extra='allow',  # Allow extra fields from hackathon tester
        str_strip_whitespace=True
    )
    
    sessionId: str
    message: MessageObj
    conversationHistory: List[MessageObj] = []
    metadata: Optional[MetadataObj] = None

# For the Dashboard/Internal use (extends basic reply)
class AgentAPIResponse(BaseModel):
    status: str
    reply: str
    # Hidden fields for Dashboard (Optional)
    debug_thought: Optional[str] = None
    intelligence: Optional[dict] = None
    metrics: Optional[dict] = None

