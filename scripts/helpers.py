import pickle

import librosa


def read_obj(path):
    with open(path, "rb") as f:
        return pickle.load(f)


def extract_audio(audio, sr=8000):
    wav, sample_rate = librosa.load(audio, sr=sr)
    dur = float(len(wav) / sample_rate)
    channel = len(wav.shape)
    wav_return = wav
    return wav_return
