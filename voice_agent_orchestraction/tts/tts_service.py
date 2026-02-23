from livekit.plugins import elevenlabs
from livekit.plugins.elevenlabs import VoiceSettings
import os
import logging

logger = logging.getLogger(__name__)


def get_tts():
    """Get ElevenLabs TTS instance"""
    if os.getenv("ELEVENLABS_API_KEY"):
        tts = elevenlabs.TTS(
            voice_id=os.getenv("ELEVENLABS_VOICE_ID"),
            model="eleven_flash_v2_5",
            api_key=os.getenv("ELEVENLABS_API_KEY"),
            voice_settings=VoiceSettings(
                stability=0.8,
                similarity_boost=0.75,
                speed=0.9,
            ),
        )
        return tts
    return None
