from dotenv import load_dotenv
import os
import asyncio
import time
import logging
from livekit import agents

logger = logging.getLogger(__name__)
from livekit.agents import AgentSession, Agent, RoomInputOptions
from voice_agent_orchestraction.stt.stt_service import get_stt
from voice_agent_orchestraction.llm.llm_service import get_llm
from voice_agent_orchestraction.tts.tts_service import get_tts
from livekit.plugins.turn_detector.multilingual import MultilingualModel
from livekit.plugins import silero, noise_cancellation
from voice_agent_orchestraction.rag.retrival import initialize, get_tools, get_prompt_file_path
from voice_agent_orchestraction.utils.transcription_logger import TranscriptionLogger, setup_transcription_logging

load_dotenv()

INITIAL_GREETING_ENABLED = os.getenv("INITIAL_GREETING_ENABLED", "true").lower() == "true"


async def entrypoint(ctx: agents.JobContext):
    await initialize()
    tools = get_tools()
    
    prompt_file_path = get_prompt_file_path()
    with open(prompt_file_path, "r", encoding="utf-8") as f:
        instructions = f.read().strip()
    
    instructions += (
        "\n\n⚠️ CRITICAL RAG POLICY - MANDATORY TOOL USAGE: "
        "Before answering ANY question about HDFC ERGO, you MUST first call the RAG_RETRIEVER tool. "
        "This includes but is not limited to:\n"
        "- Contact information (addresses, phone numbers, email addresses, office locations, branch addresses)\n"
        "- Policy details, procedures, requirements, or operations\n"
        "- Specific policy terms, coverage details, claim procedures\n"
        "- Network hospitals, exclusions, optional covers\n"
        "- ANY factual information about HDFC ERGO that requires verification\n\n"
        "This is MANDATORY for every substantive question. "
        "Do NOT rely on your training data or previous responses. "
        "Do NOT assume you know the answer. "
        "ALWAYS call RAG first, then paraphrase the response naturally. "
        "The only exceptions are: simple greetings, acknowledgments, and off-topic questions. "
        "When in doubt whether to call RAG, ALWAYS call it. "
        "NEVER mention RAG to customers - call it silently and respond as if you naturally know the information."
    )
    
    class Assistant(Agent):
        def __init__(self, tools=None) -> None:
            # Pass tools to Agent constructor (like ref.py line 844)
            super().__init__(instructions=instructions, tools=tools)
    
    session = AgentSession(
        stt=get_stt(),
        llm=get_llm(),  # Remove tools from here - tools go to Agent
        tts=get_tts(),
        # vad=silero.VAD.load(),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(tools=tools),  # Pass tools to Assistant (like ref.py line 1764)
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    session._greeting_in_progress = False
    session._greeting_start_time = None

    # Custom handler for greeting interruption check
    def greeting_check_handler(event):
        """Check for greeting interruption before logging"""
        if session._greeting_in_progress and session._greeting_start_time:
            if time.time() - session._greeting_start_time < 0.3:
                return False  # Skip logging if greeting just started
            session._greeting_in_progress = False
        return True  # Continue with logging

    # Setup transcription logging using utility module
    transcription_logger, logged_say = setup_transcription_logging(
        session, 
        custom_user_handler=greeting_check_handler
    )

    await ctx.connect()

    if INITIAL_GREETING_ENABLED:
        try:
            # Disable audio input temporarily to avoid interruptions
            session.input.set_audio_enabled(False)
            
            # Use session.say() for direct text-to-speech greeting - Sales pitch for outbound call
            greeting_text = "Hello This is Priya from Hdfc Ergo I'm reaching out because you recently showed interest in health insurance I'm here to help you understand mai Optima Secure plan which gives 4X coverageis this a good time to talk?"
            await session.say(greeting_text, allow_interruptions=True)
            
            # Re-enable audio input after greeting
            await asyncio.sleep(0.3)  # Small delay to ensure greeting completes
            session.input.set_audio_enabled(True)
        except Exception as e:
            logger.error(f"Error during initial greeting: {e}")
            session.input.set_audio_enabled(True)  # Ensure audio is re-enabled on error


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(
        agent_name="HDFC-Insurance-Agent",
        entrypoint_fnc=entrypoint,
        )
    )
