import librosa
import os
import sys
from log_helper import App_Logger
sys.path.insert(0, '../logs/')
sys.path.append(os.path.abspath(os.path.join('..')))


class DataLoader:

    def __init__(self) -> None:
        my_logger = App_Logger("../logs/henok_dat_loader.log")
        self.logger = my_logger.get_app_logger()

    def transcription_loader(self, filename):
        name_to_text = {}
        with open(filename, encoding="utf-8") as f:
            for line in f:
                name = line.split("</s>")[1]
                name = name.replace('(', '')
                name = name.replace(')', '')
                name = name.replace('\n', '')
                name = name.replace(' ', '')
                text = line.split("</s>")[0]
                text = text.replace("<s>", "")
                name_to_text[name] = text
            self.logger(f"audio-transcription pairs generated")
            return name_to_text

    def audio_metadata_generator(self, transcription, path):
        target = []
        features = []
        filenames = []
        duration_of_recordings = []
        for key in transcription:
            filename = path + key + ".wav"
            filenames.append(filename)
            audio, fs = librosa.load(filename, sr=None)
            duration_of_recordings.append(librosa.get_duration(y=audio, sr=fs))
            label = transcription[key]
            target.append(label)
        self.logger(f"audio-metadata generated")
        return filenames, target, duration_of_recordings
