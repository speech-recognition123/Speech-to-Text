from log_help import App_Logger
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
from os.path import exists
import wave
import array
sys.path.insert(0, "../logs/")
sys.path.append(os.path.abspath(os.path.join("..")))


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
            x[:, 1] == samples[hop_length: (hop_length + fft_length)]
        )

        # broadcast window, compute fft over columns and square mod
        x = np.fft.rfft(x * window, axis=0)
        x = np.absolute(x) ** 2

        # scale, 2.0 for everything except dc and fft_length/2
        x[1:-1, :] *= 2.0 / scale
        x[(0, -1), :] /= scale

        freqs = float(sample_rate) / fft_length * np.arange(x.shape[0])

        return x, freqs

    def change_channel_to_stereo(self, file1, output):
        try:
            ifile = wave.open(file1)
            print(ifile.getparams())
            # (1, 2, 44100, 2013900, 'NONE', 'not compressed')
            (nchannels, sampwidth, framerate, nframes,
             comptype, compname) = ifile.getparams()
            assert comptype == 'NONE'  # Compressed not supported yet
            array_type = {1: 'B', 2: 'h', 4: 'l'}[sampwidth]
            left_channel = array.array(array_type, ifile.readframes(nframes))[
                ::nchannels]
            ifile.close()

            stereo = 2 * left_channel
            stereo[0::2] = stereo[1::2] = left_channel

            ofile = wave.open(output, 'w')
            ofile.setparams(
                (2, sampwidth, framerate, nframes, comptype, compname))
            print(ofile.getnchannels())
            ofile.writeframes(stereo.tobytes())
            ofile.close()
            self.logger.info(
                f"Successfully changed channel to stereo for audio : {file1}")
            return ofile.getnchannels()

        except Exception as e:
            print(e)

    def resize_audio(self, audio: np.array, size: int) -> np.array:
        """
        This resizes all input audio to a fixed sample size.
        It helps us to have a consistent data shape

        Args:
            audio: This is the audio sample as a numpy array
        """
        resized = librosa.util.fix_length(audio, size, axis=1)
        print(f"Audio resized to {size} samples")
        return resized

    def meta_data(self, trans, path):
        target = []
        features = []
        mode = []
        rmse = []
        spec_cent = []
        spec_bw = []
        rolloff = []
        zcr = []
        mfcc = []
        rate = []
        filenames = []
        duration_of_recordings = []
        for index, k in enumerate(trans):
            if index < 5:
                filename = path + k + ".wav"
                next_file_name = path + k + "changed.wav"
                if exists(filename):
                    # stereo = change_channel_to_stereo(filename, next_file_name)
                    filenames.append(filename)
                    audio, fs = librosa.load(filename, sr=44100)
                    chroma_stft = librosa.feature.chroma_stft(y=audio, sr=fs)
                    rmse.append(np.mean(librosa.feature.rms(y=audio)))
                    spec_cent.append(
                        np.mean(librosa.feature.spectral_centroid(y=audio, sr=fs)))
                    spec_bw.append(
                        np.mean(librosa.feature.spectral_bandwidth(y=audio, sr=fs)))
                    rolloff.append(
                        np.mean(librosa.feature.spectral_rolloff(y=audio, sr=fs)))
                    zcr.append(
                        np.mean(librosa.feature.zero_crossing_rate(audio)))
                    mfcc.append(np.mean(librosa.feature.mfcc(y=audio, sr=fs)))
                    duration_of_recordings.append(float(len(audio)/fs))
                    rate.append(fs)
                    mode.append('mono')  # if stereo == 1 else 'stereo')
                    lable = trans[k]
                    target.append(lable)
        self.logger.info(f"Meta Data Generated For {len(filenames)} Audios")
        return filenames, target, duration_of_recordings, mode, rmse, spec_cent, spec_bw, rolloff, zcr, mfcc, rate
