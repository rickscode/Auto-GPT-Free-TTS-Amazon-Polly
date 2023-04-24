"""Polly TTS module."""
import os

import boto3
from playsound import playsound

from autogpt.config import Config
from autogpt.speech.base import VoiceBase


class PollyVoice(VoiceBase):
    """Polly TTS Voice."""

    def _setup(self) -> None:
        """Set up the voices, API key, etc."""
        cfg = Config()
        self._client = boto3.client(
            "polly",
            aws_access_key_id=cfg.aws_access_key_id,
            aws_secret_access_key=cfg.aws_secret_access_key,
            # region_name=cfg.aws_region_name,
        )
        self._voices = [
            "Amy",
            "Emma",
            "Nicole",
            "Russell",
            "Brian",
            "Aditi",
            "Raveena",
            "Joanna",
            "Ivy",
            "Kendra",
            "Kimberly",
            "Matthew",
            "Salli",
            "Joey",
            "Justin",
            "Miguel",
            "Penelope",
            "Astrid",
            "Gwyneth",
            "Maxim",
            "Lea",
            "Lucia",
            "Hans",
            "Marlene",
            "Vicki",
            "Conchita",
            "Enrique",
            "Carla",
            "Giorgio",
            "Tatyana",
            "Maja",
            "Jan",
            "Liv",
            "Lotus",
            "Ruben",
            "Ewa",
            "Ines",
        ]
        voice_id = int(cfg.aws_voice_id)
        if voice_id < 0 or voice_id >= len(self._voices):
            print(
                f"Invalid voice index {voice_id}, defaulting to voice index 0 (Amy)."
            )
            voice_id = 0
        self._voice_id = voice_id
        print(f"Using voice ID: {self._voices[self._voice_id]}")


    def _speech(self, text: str, voice_index: int = 0) -> bool:
        """Play the given text."""
        response = self._client.synthesize_speech(
            OutputFormat="mp3", Text=text, VoiceId=self._voices[voice_index]
        )



        if "AudioStream" in response:
            with open("speech.mp3", "wb") as f:
                f.write(response["AudioStream"].read())
            playsound("speech.mp3", True)
            os.remove("speech.mp3")
            return True
        else:
            print("Request failed with status code:", response.status_code)
            print("Response content:", response.content)
            return False

            