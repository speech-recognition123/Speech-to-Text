import numpy as np
import librosa
import os
import sys
from log_helper import App_Logger
sys.path.insert(0, '../logs/')
sys.path.append(os.path.abspath(os.path.join('..')))


class AudioCleaner:

    def __init__(self) -> None:
        my_logger = App_Logger("../logs/henok_audio_cleaner.log")
        self.logger = my_logger.get_app_logger()

    def resize_audio(self, audio: np.Array, size: int) -> np.array:
        """
        This resizes all input audio to a fixed sample size.
        It helps us to have a consistent data shape
        """
        resized = librosa.utils.fix_length(audio, size, axis=1)
        self.logger.info(f"Audio resized to {size} samples")
        return resized

    # def convert_to_sterio(self, audio: np.Array) -> np.Array:
