"""

This module is supposed to read the target
transcriptions and generate a dict housing the metadata about our dataset

This includes the relative path to the audio files, the text, and audio length

Jun-3-2022

author: Henok
"""


class MetaDataLoader:

    # def __init__(self) -> None:
        # my_logger = App_Logger("../logs/henok_dat_loader.log")
        # self.logger = my_logger.get_app_logger()

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
            # self.logger(f"audio-transcription pairs generated")
            return name_to_text


    def audio_metadata_generator(self, trans, path):
        metadata = []
        
        for index, k in enumerate(trans):
            sr = 44100
            filename = os.path.join(path, k + ".wav")
            if os.path.exists(filename):
                audio, fs = librosa.load(filename, sr=sr)
                # chroma_stft = librosa.feature.chroma_stft(y = audio, sr = fs)
                # rmse = np.mean(librosa.feature.rms(y = audio))
                # spec_cent = np.mean(librosa.feature.spectral_centroid(y = audio, sr = fs))
                # spec_bw = np.mean(librosa.feature.spectral_bandwidth(y = audio, sr = fs))
                # rolloff = np.mean(librosa.feature.spectral_rolloff(y = audio, sr = fs))
                # zcr = np.mean(librosa.feature.zero_crossing_rate(audio))
                # mfcc = np.mean(librosa.feature.mfcc(y = audio, sr = fs))
                duration_of_recordings = float(len(audio)/fs)
                lable = trans[k]
                
                metadata.append({
                    "filenames": filename,
                    # "rmse": rmse,
                    # "spec_cent": spec_cent,
                    # "spec_bw": spec_bw,
                    # "rolloff": rolloff,
                    # "zcr": zcr,
                    # "mfcc": mfcc,
                    "duration_of_recordings": duration_of_recordings,
                    # "rate": sr,
                    "target": lable,
                    "target_len": len(lable),
                })
            else: print(filename)
        return metadata

    def get_metadata(self, ts_file_path, wav_path, save=False, path=None):
      """
      This would take in the trainsction text file path and
      the wav audios folder path. It would then return a dictionary
      With a bunch of metadata for the two per sample
      """
      name_to_text = self.transcription_loader(ts_file_path)
      metadata = self.audio_metadata_generator(name_to_text, wav_path)
      if save:
          with open(path, 'w') as f:
              json.dump(metadata, f)
      return metadata



