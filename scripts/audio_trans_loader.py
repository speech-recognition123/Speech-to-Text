import os
import sys

import IPython.display as ipd
import librosa  # for audio processing
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from librosa.core import audio
from numpy.lib.stride_tricks import as_strided
from scipy.io import wavfile  # for audio processing

sys.path.insert(0, "../logs/")
sys.path.append(os.path.abspath(os.path.join("..")))

from log_helper import App_Logger

app_logger = App_Logger("../logs/audio_loader.log").get_app_logger()


class AudioLoader:
    def __init__(self) -> None:
        self.logger = App_Logger("../logs/audio_loader.log").get_app_logger()

    def text_length(self, df: pd.DataFrame, column: str) -> list:
        """
        # Calculates the length of the text in the given column
        # @param df: The dataframe containing the text
        # @param column: The column containing the text
        # @return: The length of the text in the given column
        """
        length_text = []

        for i in df[column]:
            length_text.append(len(i))
            self.logger.info(
                f"Calculate the length of the text in the dataframe"
            )
        return length_text

    def loaderTrans(self, filename: str):
        """
        # Loads the audio file and returns the audio data and sample rate
        # @param filename: The path to the audio file
        # @return: The audio data and sample rate
        #
        """
        name_to_text = {}
        with open(filename, encoding="utf-8") as f:
            for line in f:
                name = line.split("</s>")[1]
                name = name.replace("(", "")
                name = name.replace(")", "")
                name = name.replace("\n", "")
                name = name.replace(" ", "")
                text = line.split("</s>")[0]
                text = text.replace("<s>", "")
                name_to_text[name] = text
                self.logger.info(f"Training data loaded: {name}")
        return name_to_text

    def duration_target(self, trans, path: str):
        """
        #
        """
        target = []
        features = []
        filenames = []
        duration_of_recordings = []
        for k in trans:
            filename = path + k + ".wav"
            filenames.append(filename)
            audio, fs = librosa.load(filename, sr=None)
            duration_of_recordings.append(float(len(audio) / fs))
            lable = trans[k]
            target.append(lable)
            self.logger.info(f"divide duration of recording with there target")
        return filenames, target, duration_of_recordings

    def opens(self, audio_file_loc, sr=22000):
        samples, sample_rate = librosa.load(audio_file_loc, sr=sr)
        return (samples, sample_rate)

    def play_audio(self, samples, sample_rate):
        return ipd.Audio(samples, rate=sample_rate)

    def spectrogram(
        self, samples, fft_length=256, sample_rate=2, hop_length=128
    ):

        assert not np.iscomplexobj(samples), "Must not pass in complex numbers"

        window = np.hanning(fft_length)[:, None]
        window_norm = np.sum(window**2)

        # The scaling below follows the convention of
        # matplotlib.mlab.specgram which is the same as
        # matlabs specgram.
        scale = window_norm * sample_rate

        trunc = (len(samples) - fft_length) % hop_length
        x = samples[: len(samples) - trunc]

        # "stride trick" reshape to include overlap
        nshape = (fft_length, (len(x) - fft_length) // hop_length + 1)
        nstrides = (x.strides[0], x.strides[0] * hop_length)
        x = as_strided(x, shape=nshape, strides=nstrides)

        # window stride sanity check
        assert np.all(
            x[:, 1] == samples[hop_length : (hop_length + fft_length)]
        )

        # broadcast window, compute fft over columns and square mod
        x = np.fft.rfft(x * window, axis=0)
        x = np.absolute(x) ** 2

        # scale, 2.0 for everything except dc and fft_length/2
        x[1:-1, :] *= 2.0 / scale
        x[(0, -1), :] /= scale

        freqs = float(sample_rate) / fft_length * np.arange(x.shape[0])

        return x, freqs
