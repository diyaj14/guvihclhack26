from livekit.agents import llm
import aiohttp
import json
import logging

logger = logging.getLogger("vigilante-llm")

class VigilanteLLM(llm.LLM):
    def __init__(self, api_url, api_key, session_id):
        # Initialize parent
        super().__init__()
        self.api_url = api_url
        self.api_key = api_key
        self.session_id = session_id

    async def chat(
        self,
        chat_ctx: llm.ChatContext,
        fnc_ctx: llm.FunctionContext | None = None,
        temperature: float | None = None,
        n: int | None = None,
        parallel_tool_calls: bool | None = None,
    ) -> llm.LLMStream:
        
        # 1. Convert context to API format
        history = []
        user_msg = None
        
        # chat_ctx.messages contains the history
        # We need to skip the last message if it is the current user prompt (logic varies by SDK, usually it IS included)
        # We'll treat the last message from user as the "message" payload
        
        ordered_msgs = chat_ctx.messages
        # Find the last user message
        last_user_idx = -1
        for i in range(len(ordered_msgs) -1, -1, -1):
            if ordered_msgs[i].role == llm.ChatRole.USER:
                last_user_idx = i
                break
        
        if last_user_idx != -1:
            user_msg = ordered_msgs[last_user_idx].text
            # All previous messages are history
            # But we must preserve order.
            # API expects: conversationHistory = [ {sender:..., text:...} ... ]
            
            # Helper to map role
            def map_role(r):
                return "scammer" if r == llm.ChatRole.USER else "user"

            for i in range(last_user_idx):
                msg = ordered_msgs[i]
                if msg.text:
                    history.append({
                        "sender": map_role(msg.role),
                        "text": msg.text,
                        "timestamp": 1234567890 # Placeholder
                    })
        
        if not user_msg:
             return llm.LLMStream(self._simulate_stream("..."))

        # 2. Call API
        payload = {
            "sessionId": self.session_id,
            "message": {
                "sender": "scammer",
                "text": user_msg,
                "timestamp": 1770005528731
            },
            "conversationHistory": history
        }
        
        headers = {"x-api-key": self.api_key}
        
        logger.info(f"Sending to API: {user_msg}")
        
        reply = "I'm having trouble connecting."
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.api_url, json=payload, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        reply = data.get("reply", "I didn't hear that.")
                        logger.info(f"API Reply: {reply}")
                    else:
                        txt = await resp.text()
                        logger.error(f"API Error {resp.status}: {txt}")
        except Exception as e:
            logger.error(f"API Exception: {e}")

        # 3. Return Stream
        return llm.LLMStream(self._simulate_stream(reply))

    async def _simulate_stream(self, text):
        # Yield the text as a single chunk (or we could split it)
        # LiveKit TTS handles full sentences well.
        yield llm.ChatChunk(choices=[llm.Choice(delta=llm.ChoiceDelta(content=text, role=llm.ChatRole.ASSISTANT))])
