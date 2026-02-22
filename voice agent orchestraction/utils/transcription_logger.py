"""
Transcription Logger Utility

Handles logging of both user and agent transcriptions to file and console.
Supports LiveKit AgentSession events for capturing speech-to-text and text-to-speech.
"""

import os
import time
import logging
from datetime import datetime
from typing import Optional, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class TranscriptionLogger:
    """Handles transcription logging for user and agent conversations"""
    
    def __init__(
        self,
        log_file: Optional[str] = None,
        enabled: bool = True
    ):
        """
        Initialize transcription logger
        
        Args:
            log_file: Path to log file (default: transcriptions.log in current directory)
            enabled: Whether logging is enabled
        """
        self.enabled = enabled
        self.log_file = log_file or os.getenv(
            "TRANSCRIPTION_LOG_FILE", 
            str(Path(__file__).parent.parent / "transcriptions.log")
        )
        
        # Ensure log file directory exists
        log_path = Path(self.log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Transcription logger initialized: enabled={enabled}, file={self.log_file}")
    
    def log(self, speaker: str, text: str, timestamp: Optional[float] = None):
        """
        Log transcription to file and console
        
        Args:
            speaker: Speaker identifier (USER, AGENT, etc.)
            text: Transcription text
            timestamp: Optional timestamp (defaults to current time)
        """
        if not self.enabled:
            return
        
        if not text or not text.strip():
            return
        
        if timestamp is None:
            timestamp = time.time()
        
        # Format timestamp
        dt = datetime.fromtimestamp(timestamp)
        timestamp_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        
        # Create log entry
        log_entry = f"[{timestamp_str}] {speaker}: {text.strip()}\n"
        
        # Write to file
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_entry)
        except Exception as e:
            logger.error(f"Failed to write transcription to file: {e}")
        
        # Log to console
        logger.info(f"📝 TRANSCRIPTION - {speaker}: {text.strip()}")
    
    def log_user_transcription(self, event: Any):
        """
        Extract and log user transcription from LiveKit event
        
        Args:
            event: LiveKit user_input_transcribed event
        """
        try:
            # Try different event attributes based on LiveKit structure
            user_text = None
            
            # Check for transcript attribute (common in LiveKit) - highest priority
            if hasattr(event, 'transcript'):
                user_text = event.transcript
            # Check for transcription object
            elif hasattr(event, 'transcription') and event.transcription:
                if hasattr(event.transcription, 'text'):
                    user_text = event.transcription.text
                elif hasattr(event.transcription, 'transcript'):
                    user_text = event.transcription.transcript
                else:
                    user_text = str(event.transcription)
            # Check for text attribute
            elif hasattr(event, 'text'):
                user_text = event.text
            # Check for message attribute
            elif hasattr(event, 'message'):
                user_text = event.message
            # Fallback: try to extract from string representation
            else:
                event_str = str(event)
                # Try to extract transcript from event string (handles both ' and " quotes)
                if "transcript='" in event_str:
                    start = event_str.find("transcript='") + len("transcript='")
                    end = event_str.find("'", start)
                    if end > start:
                        user_text = event_str[start:end]
                elif 'transcript="' in event_str:
                    start = event_str.find('transcript="') + len('transcript="')
                    end = event_str.find('"', start)
                    if end > start:
                        user_text = event_str[start:end]
                elif "transcript=" in event_str:
                    # Try to extract without quotes
                    start = event_str.find("transcript=") + len("transcript=")
                    # Find the end (space, comma, or end of string)
                    end = len(event_str)
                    for char in [' ', ',', '}', ')', '\n']:
                        idx = event_str.find(char, start)
                        if idx != -1 and idx < end:
                            end = idx
                    if end > start:
                        user_text = event_str[start:end].strip()
            
            if user_text and user_text.strip():
                self.log("USER", user_text.strip())
            else:
                logger.debug(f"Could not extract user text from event. Event type: {type(event)}, Attributes: {dir(event) if hasattr(event, '__dict__') else 'N/A'}")
        except Exception as e:
            logger.debug(f"Could not extract user transcription: {e}", exc_info=True)
    
    def log_agent_response(self, text: str):
        """
        Log agent response text (from LLM before TTS)
        
        Args:
            text: Agent response text
        """
        if text and text.strip():
            self.log("AGENT", text.strip())
    
    def log_agent_speech(self, event: Any):
        """
        Extract and log agent speech from LiveKit event
        
        Args:
            event: LiveKit agent speech event
        """
        try:
            agent_text = None
            
            # Check for text attribute
            if hasattr(event, 'text') and event.text:
                agent_text = event.text
            # Check for transcription object
            elif hasattr(event, 'transcription') and event.transcription:
                if hasattr(event.transcription, 'text'):
                    agent_text = event.transcription.text
                else:
                    agent_text = str(event.transcription)
            # Check for message attribute
            elif hasattr(event, 'message'):
                agent_text = event.message
            
            if agent_text and agent_text.strip():
                self.log("AGENT (TTS)", agent_text.strip())
            else:
                logger.debug(f"Could not extract agent text from event: {event}")
        except Exception as e:
            logger.debug(f"Could not extract agent speech transcription: {e}")


def setup_transcription_logging(
    session, 
    logger_instance: Optional[TranscriptionLogger] = None,
    custom_user_handler: Optional[callable] = None
):
    """
    Setup transcription logging for a LiveKit AgentSession
    
    Args:
        session: LiveKit AgentSession instance
        logger_instance: Optional TranscriptionLogger instance (creates new one if not provided)
        custom_user_handler: Optional custom function to call before logging user transcription
    
    Returns:
        TranscriptionLogger instance and wrapped session.say function
    """
    if logger_instance is None:
        enabled = os.getenv("TRANSCRIPTION_LOG_ENABLED", "true").lower() == "true"
        logger_instance = TranscriptionLogger(enabled=enabled)
    
    # Wrap session.say to capture agent responses
    original_say = session.say
    
    async def logged_say(text: str, **kwargs):
        """Wrapper around session.say to log agent speech"""
        logger_instance.log_agent_response(text)
        return await original_say(text, **kwargs)
    
    session.say = logged_say
    
    # Setup user transcription event handler
    @session.on("user_input_transcribed")
    def on_user_input_transcribed(event):
        """Handle user speech transcription"""
        # Call custom handler if provided (e.g., for greeting check)
        # If handler returns False, skip logging
        should_log = True
        if custom_user_handler:
            try:
                result = custom_user_handler(event)
                if result is False:
                    should_log = False
            except Exception as e:
                logger.debug(f"Custom user handler raised exception: {e}")
        
        # Log user transcription if handler didn't skip it
        if should_log:
            logger_instance.log_user_transcription(event)
    
    # Try to setup agent speech event handlers
    try:
        @session.on("agent_speech_committed")
        def on_agent_speech_committed(event):
            """Handle agent speech transcription (what agent said)"""
            logger_instance.log_agent_speech(event)
    except Exception as e:
        logger.debug(f"Could not register agent_speech_committed event: {e}")
    
    # Try alternative event names
    for event_name in ["agent_response", "agent_speech", "tts_complete"]:
        try:
            @session.on(event_name)
            def on_agent_event(event):
                """Handle agent event"""
                logger_instance.log_agent_speech(event)
            logger.info(f"Registered transcription handler for event: {event_name}")
            break
        except Exception as e:
            logger.debug(f"Could not register {event_name} event: {e}")
    
    return logger_instance, logged_say
