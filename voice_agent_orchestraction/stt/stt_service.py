from livekit.plugins import deepgram
import os


def get_stt():
    return deepgram.STT(
        api_key=os.getenv("DEEPGRAM_API_KEY"),
        model="nova-3",
        language="multi",
    )