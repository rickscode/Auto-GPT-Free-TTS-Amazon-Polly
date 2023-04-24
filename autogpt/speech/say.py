""" Text to speech module """
import threading
from threading import Semaphore

from autogpt.config import Config
from autogpt.speech.brian import BrianSpeech
from autogpt.speech.eleven_labs import ElevenLabsSpeech
from autogpt.speech.gtts import GTTSVoice
from autogpt.speech.macos_tts import MacOSTTS
from autogpt.speech.aws_polly import PollyVoice

CFG = Config()
DEFAULT_VOICE_ENGINE = GTTSVoice()
VOICE_ENGINE = None

if CFG.elevenlabs_api_key:
    VOICE_ENGINE = ElevenLabsSpeech()
elif CFG.aws_access_key_id and CFG.aws_secret_access_key and CFG.aws_region_name and CFG.aws_voice_id:
    print('Polly Enabled')
    VOICE_ENGINE = PollyVoice()
elif CFG.use_mac_os_tts == "True":
    VOICE_ENGINE = MacOSTTS()
elif CFG.use_brian_tts == "True":
    VOICE_ENGINE = BrianSpeech()
else:
    VOICE_ENGINE = GTTSVoice()

QUEUE_SEMAPHORE = Semaphore(
    1
)  # The amount of sounds to queue before blocking the main thread


def speak(text: str, voice_index: int = 0) -> None:
    success = VOICE_ENGINE.say(text, voice_index)
    print(VOICE_ENGINE)
    if not success:
        DEFAULT_VOICE_ENGINE.say(text)

    QUEUE_SEMAPHORE.release()

def say_text(text: str, voice_index: int = 0) -> None:
    """Speak the given text using the given voice index"""

    QUEUE_SEMAPHORE.acquire(True)
    thread = threading.Thread(target=speak, args=(text,))
    thread.start()
