"""
Defines a class that is used to predict trancription text from a model
and calculate various performance metrics of the model.
"""
import numpy as np
import pandas as pd
import soundfile
import json

import random
from python_speech_features import mfcc
import librosa
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
class Prediction():

    
    def predict_raw(data_gen, index, partition, model):
        """ Get a model's decoded predictions
        Params:
            data_gen: Data to run prediction on
            index (int): Example to visualize
            partition (str): Either 'train' or 'validation'
            model (Model): The acoustic model
        """

        if partition == 'validation':
            transcr = data_gen.valid_texts[index]
            audio_path = data_gen.valid_audio_paths[index]
            data_point = data_gen.normalize(data_gen.featurize(audio_path))
        elif partition == 'train':
            transcr = data_gen.train_texts[index]
            audio_path = data_gen.train_audio_paths[index]
            data_point = data_gen.normalize(data_gen.featurize(audio_path))
        else:
            raise Exception('Invalid partition!  Must be "train" or "validation"')
            
        prediction = model.predict(np.expand_dims(data_point, axis=0))
        return (audio_path,data_point,transcr,prediction)

    def int_sequence_to_text(int_sequence):
        """ Convert an integer sequence to text """
        text = []
        for c in int_sequence:
            ch = index_map[c]
            text.append(ch)
        return text
    # Code adapted from https://martin-thoma.com/word-error-rate-calculation/
    def wer(r, h):
        """
        Calculation of WER with Levenshtein distance.

        Works only for iterables up to 254 elements (uint8).
        O(nm) time ans space complexity.

        Parameters
        ----------
        r : list
        h : list

        Returns
        -------
        int

        Examples
        --------
        >>> wer("who is there".split(), "is there".split())
        1
        >>> wer("who is there".split(), "".split())
        3
        >>> wer("".split(), "who is there".split())
        3
        """
        # initialisation
        import numpy
        d = numpy.zeros((len(r)+1)*(len(h)+1), dtype=numpy.uint8)
        d = d.reshape((len(r)+1, len(h)+1))
        for i in range(len(r)+1):
            for j in range(len(h)+1):
                if i == 0:
                    d[0][j] = j
                elif j == 0:
                    d[i][0] = i

        # computation
        for i in range(1, len(r)+1):
            for j in range(1, len(h)+1):
                if r[i-1] == h[j-1]:
                    d[i][j] = d[i-1][j-1]
                else:
                    substitution = d[i-1][j-1] + 1
                    insertion    = d[i][j-1] + 1
                    deletion     = d[i-1][j] + 1
                    d[i][j] = min(substitution, insertion, deletion)

        return d[len(r)][len(h)]
    def calculate_wer(model, model_name, data_gen, partition, length):
        start = time.time()
        def wer_single(i):
            wer = predict(data_gen, i, partition, model, verbose=False)
            if (i%100==0) and i>0:
                print("processed %d in %d minutes" % (i, ((time.time() - start)/60)))
            return wer
        wer = list(map(lambda i: wer_single(i), range(1, length)))
        print("Total time: %f minutes" % ((time.time() - start)/60))
        filename = 'models/' + model_name + '_' + partition + '_wer.pickle'
        with open(filename, 'wb') as handle:
            pickle.dump(wer, handle)
        return wer


    def load_wer(model_name, partition):
        filename = 'models/' + model_name + '_' + partition + '_wer.pickle'
        return pickle.load(open(filename, "rb"))

    def spectrogram(samples, fft_length=256, sample_rate=2, hop_length=128):
        """
        Compute the spectrogram for a real signal.
        The parameters follow the naming convention of
        matplotlib.mlab.specgram

        Args:
            samples (1D array): input audio signal
            fft_length (int): number of elements in fft window
            sample_rate (scalar): sample rate
            hop_length (int): hop length (relative offset between neighboring
                fft windows).

        Returns:
            x (2D array): spectrogram [frequency x time]
            freq (1D array): frequency of each row in x

        Note:
            This is a truncating computation e.g. if fft_length=10,
            hop_length=5 and the signal has 23 elements, then the
            last 3 elements will be truncated.
        """
        assert not np.iscomplexobj(samples), "Must not pass in complex numbers"

        window = np.hanning(fft_length)[:, None]
        window_norm = np.sum(window**2)

        # The scaling below follows the convention of
        # matplotlib.mlab.specgram which is the same as
        # matlabs specgram.
        scale = window_norm * sample_rate

        trunc = (len(samples) - fft_length) % hop_length
        x = samples[:len(samples) - trunc]

        # "stride trick" reshape to include overlap
        nshape = (fft_length, (len(x) - fft_length) // hop_length + 1)
        nstrides = (x.strides[0], x.strides[0] * hop_length)
        x = as_strided(x, shape=nshape, strides=nstrides)

        # window stride sanity check
        assert np.all(x[:, 1] == samples[hop_length:(hop_length + fft_length)])

        # broadcast window, compute fft over columns and square mod
        x = np.fft.rfft(x * window, axis=0)
        x = np.absolute(x)**2

        # scale, 2.0 for everything except dc and fft_length/2
        x[1:-1, :] *= (2.0 / scale)
        x[(0, -1), :] /= scale

        freqs = float(sample_rate) / fft_length * np.arange(x.shape[0])

        return x, freqs
    def spectrogram_from_file(filename, step=10, window=20, max_freq=None,
                            eps=1e-14):
        """ Calculate the log of linear spectrogram from FFT energy
        Params:
            filename (str): Path to the audio file
            step (int): Step size in milliseconds between windows
            window (int): FFT window size in milliseconds
            max_freq (int): Only FFT bins corresponding to frequencies between
                [0, max_freq] are returned
            eps (float): Small value to ensure numerical stability (for ln(x))
        """
        with soundfile.SoundFile(filename) as sound_file:
            audio = sound_file.read(dtype='float32')
            sample_rate = sound_file.samplerate
            if audio.ndim >= 2:
                audio = np.mean(audio, 1)
            if max_freq is None:
                max_freq = sample_rate / 2
            if max_freq > sample_rate / 2:
                raise ValueError("max_freq must not be greater than half of "
                                " sample rate")
            if step > window:
                raise ValueError("step size must not be greater than window size")
            hop_length = int(0.001 * step * sample_rate)
            fft_length = int(0.001 * window * sample_rate)
            pxx, freqs = spectrogram(
                audio, fft_length=fft_length, sample_rate=sample_rate,
                hop_length=hop_length)
            ind = np.where(freqs <= max_freq)[0][-1] + 1
        return np.transpose(np.log(pxx[:ind, :] + eps))
    def predict(data_gen, index, partition, model, verbose=True):
        """ Print a model's decoded predictions
        Params:
            data_gen: Data to run prediction on
            index (int): Example to visualize
            partition (str): Either 'train' or 'validation'
            model (Model): The acoustic model
        """
        audio_path,data_point,transcr,prediction = predict_raw(data_gen, index, partition, model)
        output_length = [model.output_length(data_point.shape[0])]
        pred_ints = (K.eval(K.ctc_decode(
                    prediction, output_length, greedy=False)[0][0])+1).flatten().tolist()
        predicted = ''.join(int_sequence_to_text(pred_ints)).replace("<SPACE>", " ")
        wer_val = wer(transcr, predicted)
        if verbose:
            display(Audio(audio_path, embed=True))
            print('Truth: ' + transcr)
            print('Predicted: ' + predicted)
            print("wer: %d" % wer_val)
        return wer_val
