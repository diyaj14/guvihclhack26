import logging
import os
import sys
import asyncio
from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice import Agent, AgentSession
from livekit.plugins import deepgram, groq, silero, cartesia
from personas import PERSONAS, get_persona

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("voice-agent")

# Windows-specific fix for "WinError 87" and asyncio issues
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def entrypoint(ctx: JobContext):
    # Connect to the room
    logger.info(f"Connecting to room {ctx.room.name}")
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # Wait for the first participant to join
    logger.info("Waiting for participant...")
    participant = await ctx.wait_for_participant()
    logger.info(f"Starting voice session for participant {participant.identity}")

    # Determine persona from participant metadata (passed from frontend)
    # Wait up to 3 seconds for metadata to sync if it's empty
    persona_key = participant.metadata
    if not persona_key:
        logger.info("Metadata not found yet, waiting for sync...")
        for _ in range(30): # 3 seconds max
            await asyncio.sleep(0.1)
            persona_key = participant.metadata
            if persona_key:
                break
    
    persona_key = persona_key or "grandma"
    selected_instructions = get_persona(persona_key)
    logger.info(f"PERSONA DETECTED: {persona_key}")
    logger.info(f"Target Identity: {participant.identity}")

    # Voice & Greeting Configuration
    # We use Deepgram Aura for stability and speed
    # Mrs. Sharma: aura-athena-en (UK accent - sounds more formal/Indian-English)
    # Ramesh: aura-orion-en (Masculine, mature male)
    # Colonel: aura-zeus-en (Extremely masculine, authoritative)
    persona_config = {
        "grandma": {
            "voice": "aura-athena-en", 
            "greeting": "Hello? Hello? I can't see who's calling... my eyes are not what they used to be."
        },
        "ramesh": {
            "voice": "aura-orion-en", 
            "greeting": "Haan, Ramesh here. Tell me quickly, I have a line of customers at the shop."
        },
        "priya": {
            "voice": "aura-luna-en", 
            "greeting": "Hey! Who is this? Long time! Wait, do I know this number?"
        },
        "colonel": {
            "voice": "aura-zeus-en", 
            "greeting": "Bakshi here. State your name. I'm in the middle of a Veteran's meeting."
        }
    }

    def create_voice_agent(key):
        cfg = persona_config.get(key, persona_config["grandma"])
        instructions = get_persona(key)
        
        return Agent(
            stt=deepgram.STT(),
            llm=groq.LLM(model="llama-3.3-70b-versatile", temperature=0.5), 
            tts=deepgram.TTS(model=cfg["voice"]),
            vad=silero.VAD.load(),
            instructions=instructions,
        )

    # Initialize first agent
    agent = create_voice_agent(persona_key)

    # Initialize the AgentSession
    session = AgentSession(
        stt=agent.stt,
        llm=agent.llm,
        tts=agent.tts,
        vad=agent.vad,
    )

    # Start the agent session in the room
    logger.info("Starting AgentSession...")
    await session.start(agent, room=ctx.room)
    logger.info("Agent session started.")

    # Initial greeting
    cfg = persona_config.get(persona_key, persona_config["grandma"])
    # Increase delay to ensure frontend is fully subscribed to the track
    await asyncio.sleep(2.0)
    
    if ctx.room.isconnected:
        logger.info(f"VERIFIED: Room is connected. Attempting to say greeting: {cfg['greeting']}")
        try:
            # Disable interruptions for the INTRO to ensure it's heard
            session.say(cfg["greeting"], allow_interruptions=False)
            logger.info("--> session.say() CALLED AND RETURNED. Audio should be flowing.")
        except Exception as e:
            logger.error(f"Failed to say greeting: {e}")
    else:
        logger.warning(f"Skipping greeting: Session state invalid (started={session._started}, closed={session._closed})")

    # --- AGENTIC HOT-SWAPPING (MULTI-VOICE) ---
    @ctx.room.on("participant_metadata_changed")
    def on_metadata_changed(p, _):
        if p.identity == participant.identity:
            new_persona = p.metadata
            if new_persona and new_persona != persona_key:
                logger.info(f"HOT-SWAP (VOICE + PERSONA): {new_persona}")
                
                async def perform_swap():
                    nonlocal persona_key
                    try:
                        # CRITICAL: Robust checks before interacting with session
                        if not ctx.room.isconnected:
                            logger.warning(f"Aborting swap: Room not connected.")
                            return

                        # Create entirely new agent with the NEW VOICE
                        new_agent = create_voice_agent(new_persona)
                        
                        # Update session to use the new agent pipeline
                        session.update_agent(new_agent)
                        
                        # Clear history
                        await new_agent.update_chat_ctx(llm.ChatContext())
                        
                        # Say new persona-specific greeting
                        new_cfg = persona_config.get(new_persona, persona_config["grandma"])
                        
                        # Use a small delay to ensure update is registered
                        await asyncio.sleep(0.5)
                        if ctx.room.isconnected:
                            logger.info(f"Swapping to voice: {new_cfg['voice']}")
                            session.say(new_cfg["greeting"], allow_interruptions=True)
                        
                        persona_key = new_persona
                        logger.info(f"SWAP COMPLETE: {new_persona} with voice {new_cfg['voice']}")
                    except Exception as e:
                        logger.error(f"Error during hot-swap: {e}")

                asyncio.create_task(perform_swap())

    # Keep the task running until THE USER leaves or the room is closed
    done_event = asyncio.Event()

    @ctx.room.on("participant_disconnected")
    def on_participant_disconnected(p):
        if p.identity == participant.identity:
            logger.info(f"User {p.identity} left. Terminating session.")
            done_event.set()

    @ctx.room.on("disconnected")
    def on_disconnected(reason):
        logger.info(f"Room disconnected: {reason}")
        done_event.set()

    # Wait for completion
    logger.info("Agent is now in the wait_for_disconnect loop. Staying alive.")
    await ctx.room.wait_for_disconnect()
    logger.info("Agent job finished (room disconnected).")

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
