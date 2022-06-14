import numpy as np
import librosa
from log import get_logger
import IPython.display as ipd
from wordcloud import WordCloud
import sklearn
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
from IPython.display import Image
from mpl_toolkits.axes_grid1 import make_axes_locatable
import librosa.display


class AudioVis():
    """Visualisation of the audio file, spectogram, mfcc....
    """

    def __init__(self):
        self.logger = get_logger("FileHandler")

    def play_audio(self, samples, sr=22000):
        return ipd.Audio(samples, rate=sr)

    def wav_plot(self, signal, title, x_label, y_label, sr=22000):
        plt.figure(figsize=(25, 5))
        librosa.display.waveplot(signal, sr=sr)
        plt.title(title)
        plt.ylabel(x_label)
        plt.xlabel(y_label)
        plt.show()

    def get_wc(self, df, column, stop_words):
        plt.figure(figsize=(30, 20))
        wordcloud = WordCloud(font_path='../fonts/NotoSansEthiopic-Medium.ttf', max_words=5000,
                              background_color="salmon", width=3000, height=2000, colormap='Pastel1',
                              collocations=False, stopwords=stop_words).generate(' '.join(df[column].values))
        plt.imshow(wordcloud)
        plt.axis('off')
        plt.title('Most Frequent Words In Amharic Audio Transcription', fontsize=16)
        plt.show()

    def plot_raw_audio(vis_raw_audio, title='Audio Signal', size=(12, 3)):
        fig = plt.figure(figsize=size)
        ax = fig.add_subplot(111)
        steps = len(vis_raw_audio)
        ax.plot(np.linspace(1, steps, steps), vis_raw_audio)
        plt.title(title)
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        plt.show()

    def plot_mfcc_feature(self, vis_mfcc_feature):
        fig = plt.figure(figsize=(12, 5))
        ax = fig.add_subplot(111)
        im = ax.imshow(vis_mfcc_feature, cmap=plt.cm.jet, aspect='auto')
        plt.title('Normalized MFCC')
        plt.ylabel('Time')
        plt.xlabel('MFCC Coefficient')
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        plt.colorbar(im, cax=cax)
        ax.set_xticks(np.arange(0, 13, 2), minor=False)
        plt.show()

    def plot_spectrogram_feature(self, vis_spectrogram_feature):
        fig = plt.figure(figsize=(12, 5))
        ax = fig.add_subplot(111)
        im = ax.imshow(vis_spectrogram_feature, cmap=plt.cm.jet, aspect='auto')
        plt.title('Normalized Spectrogram')
        plt.ylabel('Time')
        plt.xlabel('Frequency')
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        plt.colorbar(im, cax=cax)
        plt.show()

    def plot_stft(self, samples, sample_rate):
        X = librosa.stft(samples)
        Xdb = librosa.amplitude_to_db(abs(X))
        plt.figure(figsize=(14, 5))
        librosa.display.specshow(
            Xdb, sr=sample_rate, x_axis='time', y_axis='hz')
        plt.colorbar()
        plt.show()

    def normalize(self, x, axis=0):
        return sklearn.preprocessing.minmax_scale(x, axis=axis)

    def plot_spectral_centroid(self, t, spectral_centroids, samples, sample_rate):

        # Normalising the spectral centroid for visualisation
        # Plotting the Spectral Centroid along the waveform
        plt.figure(figsize=(15, 9))
        librosa.display.waveshow(samples, sr=sample_rate, alpha=0.4)
        plt.plot(t, self.normalize(spectral_centroids), color='b')
        plt.show()

    def plot_spectral_rolloff(self, t, spectral_rolloff, samples, sample_rate):
        plt.figure(figsize=(15, 9))
        librosa.display.waveshow(samples, sr=sample_rate, alpha=0.4)
        plt.plot(t, self.normalize(spectral_rolloff), color='r')
        plt.show()

    def plot_spectral_bandwidth(self, t, samples, sample_rate):
        spectral_bandwidth_2 = librosa.feature.spectral_bandwidth(
            samples+0.01, sr=sample_rate)[0]
        spectral_bandwidth_3 = librosa.feature.spectral_bandwidth(
            samples+0.01, sr=sample_rate, p=3)[0]
        spectral_bandwidth_4 = librosa.feature.spectral_bandwidth(
            samples+0.01, sr=sample_rate, p=4)[0]
        plt.figure(figsize=(15, 9))

        librosa.display.waveshow(samples, sr=sample_rate, alpha=0.4)
        plt.plot(t, self.normalize(spectral_bandwidth_2), color='r')
        plt.plot(t, self.normalize(spectral_bandwidth_3), color='g')
        plt.plot(t, self.normalize(spectral_bandwidth_4), color='y')
        plt.legend(('p = 2', 'p = 3', 'p = 4'))
        plt.show()

    def plot_spec(self, data: np.array, sr: int) -> None:
        '''
        Function for plotting spectrogram along with amplitude wave graph
        '''

        fig, ax = plt.subplots(1, 2, figsize=(15, 5))
        ax[0].title.set_text(f'Shfiting the wave by Times {sr/10}')
        ax[0].specgram(data, Fs=2)
        ax[1].set_ylabel('Amplitude')
        ax[1].plot(np.linspace(0, 1, len(data)), data)

    def plot_mfcc(self, samples, sample_rate):
        plt.figure(figsize=(20, 5))
        mfccs = librosa.feature.mfcc(samples, sr=sample_rate)
        librosa.display.specshow(mfccs, sr=sample_rate, x_axis='time')
