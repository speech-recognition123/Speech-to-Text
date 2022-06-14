import tensorflow as tf
import keras.losses
from keras import constraints, initializers, regularizers
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint
from keras.optimizers import Adam, SGD, RMSprop, Adagrad, Adadelta, Adamax, Nadam
from keras.regularizers import l2
from keras.layers import Wrapper
from keras.layers import BatchNormalization, TimeDistributed, Bidirectional
from keras.layers import LeakyReLU, PReLU, ThresholdedReLU, ELU
from keras.layers import (
    Convolution2D,
    MaxPooling2D,
    Convolution1D,
    Conv1D,
    SimpleRNN,
    GRU,
    LSTM,
    CuDNNLSTM,
    CuDNNGRU,
    Conv2D,
)
from keras.layers import (
    Input,
    Lambda,
    Dense,
    Dropout,
    Flatten,
    Embedding,
    Activation,
    GRUCell,
    LSTMCell,
    SimpleRNNCell,
)
from keras.models import Model, Sequential, load_model
from keras.constraints import max_norm
from keras import regularizers, callbacks
from keras import backend as K
from keras.utils.generic_utils import get_custom_objects
import keras
from scipy.fftpack import fft
import scipy.io.wavfile as wav
from python_speech_features import mfcc
from scipy.fftpack import dct
from scipy import signal
import json
import soundfile
from numpy.lib.stride_tricks import as_strided
from random import sample
import random
import pickle
import sys
import os
import pandas as pd
import numpy as np
from prep import prep

prep = prep()
# Audio processing
# Neural Network

# Setting Random Seeds
np.random.seed(95)
RNG_SEED = 95


class AudioGenerator:
    def __init__(
        self,
        step=10,
        window=20,
        max_freq=8000,
        mfcc_dim=13,
        minibatch_size=20,
        desc_file=None,
        spectrogram=True,
        max_duration=10.0,
        sort_by_duration=False,
    ):
        # Initializing variables
        self.feat_dim = prep.calc_feat_dim(window, max_freq)
        self.mfcc_dim = mfcc_dim
        self.feats_mean = np.zeros((self.feat_dim,))
        self.feats_std = np.ones((self.feat_dim,))
        self.rng = random.Random(RNG_SEED)
        if desc_file is not None:
            self.load_metadata_from_desc_file(desc_file)
        self.step = step
        self.window = window
        self.max_freq = max_freq
        self.cur_train_index = 0
        self.cur_valid_index = 0
        self.cur_test_index = 0
        self.max_duration = max_duration
        self.minibatch_size = minibatch_size
        self.spectrogram = spectrogram
        self.sort_by_duration = sort_by_duration

    def get_batch(self, partition):
        # Obtain a batch of audio files
        if partition == "train":
            audio_paths = self.train_audio_paths
            cur_index = self.cur_train_index
            texts = self.train_texts
        elif partition == "valid":
            audio_paths = self.valid_audio_paths
            cur_index = self.cur_valid_index
            texts = self.valid_texts
        elif partition == "test":
            audio_paths = self.test_audio_paths
            cur_index = self.test_valid_index
            texts = self.test_texts
        else:
            raise Exception("Invalid partition. Must be train/validation/test")

        features = [
            self.normalize(self.featurize(a))
            for a in audio_paths[cur_index : cur_index + self.minibatch_size]
        ]

        # Calculate size
        max_length = max([features[i].shape[0] for i in range(0, self.minibatch_size)])
        max_string_length = max(
            [len(texts[cur_index + i]) for i in range(0, self.minibatch_size)]
        )

        # Initialize arrays
        X_data = np.zeros(
            [
                self.minibatch_size,
                max_length,
                self.feat_dim * self.spectrogram
                + self.mfcc_dim * (not self.spectrogram),
            ]
        )
        labels = np.ones([self.minibatch_size, max_string_length]) * 28
        input_length = np.zeros([self.minibatch_size, 1])
        label_length = np.zeros([self.minibatch_size, 1])

        for i in range(0, self.minibatch_size):
            # Calculate input_length
            feat = features[i]
            input_length[i] = feat.shape[0]
            X_data[i, : feat.shape[0], :] = feat

            # Calculate label_length
            label = np.array(prep.text_to_int_seq(texts[cur_index + i]))
            labels[i, : len(label)] = label
            label_length[i] = len(label)

        # Output arrays
        outputs = {"ctc": np.zeros([self.minibatch_size])}
        inputs = {
            "the_input": X_data,
            "the_labels": labels,
            "input_length": input_length,
            "label_length": label_length,
        }
        return (inputs, outputs)

    def shuffle_dataset_by_partition(self, partition):
        # More shuffling
        if partition == "train":
            (
                self.train_audio_paths,
                self.train_durations,
                self.train_texts,
            ) = prep.shuffle_dataset(
                self.train_audio_paths, self.train_durations, self.train_texts
            )
        elif partition == "valid":
            (
                self.valid_audio_paths,
                self.valid_durations,
                self.valid_texts,
            ) = prep.shuffle_dataset(
                self.valid_audio_paths, self.valid_durations, self.valid_texts
            )
        else:
            raise Exception("Invalid partition. " "Must be train/val")

    def sort_dataset_by_duration(self, partition):
        # Extra shuffling
        if partition == "train":
            (
                self.train_audio_paths,
                self.train_durations,
                self.train_texts,
            ) = prep.sort_dataset(
                self.train_audio_paths, self.train_durations, self.train_texts
            )
        elif partition == "valid":
            (
                self.valid_audio_paths,
                self.valid_durations,
                self.valid_texts,
            ) = prep.sort_dataset(
                self.valid_audio_paths, self.valid_durations, self.valid_texts
            )
        else:
            raise Exception("Invalid partition. " "Must be train/val")

    def next_train(self):
        # Get a batch of training data
        while True:
            ret = self.get_batch("train")
            self.cur_train_index += self.minibatch_size
            if self.cur_train_index >= len(self.train_texts) - self.minibatch_size:
                self.cur_train_index = 0
                self.shuffle_dataset_by_partition("train")
            yield ret

    def next_valid(self):
        # Get a batch of validation data
        while True:
            ret = self.get_batch("valid")
            self.cur_valid_index += self.minibatch_size
            if self.cur_valid_index >= len(self.valid_texts) - self.minibatch_size:
                self.cur_valid_index = 0
                self.shuffle_dataset_by_partition("valid")
            yield ret

    def next_test(self):
        # Get a batch of testing data
        while True:
            ret = self.get_batch("test")
            self.cur_test_index += self.minibatch_size
            if self.cur_test_index >= len(self.test_texts) - self.minibatch_size:
                self.cur_test_index = 0
            yield ret

    # Load datasets
    def load_train_data(self, desc_file="../data/train_corpus.json"):
        self.load_metadata_from_desc_file(desc_file, "train")
        self.fit_train()
        if self.sort_by_duration:
            self.sort_dataset_by_duration("train")

    def load_validation_data(self, desc_file="../data/valid_corpus.json"):
        self.load_metadata_from_desc_file(desc_file, "validation")
        if self.sort_by_duration:
            self.sort_dataset_by_duration("valid")

    def load_test_data(self, desc_file="../data/test_corpus.json"):
        self.load_metadata_from_desc_file(desc_file, "test")
        if self.sort_by_duration:
            self.sort_dataset_by_duration("test")

    def load_metadata_from_desc_file(self, desc_file, partition):
        # Get metadata from json corpus
        audio_paths, durations, texts = [], [], []
        with open(desc_file) as json_line_file:
            for line_num, json_line in enumerate(json_line_file):
                try:
                    spec = json.loads(json_line)
                    if float(spec["duration"]) > self.max_duration:
                        continue
                    audio_paths.append(spec["key"])
                    durations.append(float(spec["duration"]))
                    texts.append(spec["text"])
                except Exception as e:
                    print("Error reading line #{}: {}".format(line_num, json_line))
        if partition == "train":
            self.train_audio_paths = audio_paths
            self.train_durations = durations
            self.train_texts = texts
        elif partition == "validation":
            self.valid_audio_paths = audio_paths
            self.valid_durations = durations
            self.valid_texts = texts
        elif partition == "test":
            self.test_audio_paths = audio_paths
            self.test_durations = durations
            self.test_texts = texts
        else:
            raise Exception("Invalid partition. " "Must be train/validation/test")

    def fit_train(self, k_samples=100):
        # Estimate descriptive stats for training set based on sample of 100 instances
        k_samples = min(k_samples, len(self.train_audio_paths))
        samples = self.rng.sample(self.train_audio_paths, k_samples)
        feats = [self.featurize(s) for s in samples]
        feats = np.vstack(feats)
        self.feats_mean = np.mean(feats, axis=0)
        self.feats_std = np.std(feats, axis=0)

    # Defining 3 different ways of converting audio files to spectrograms

    def spectrogramm(self, samples, fft_length=256, sample_rate=2, hop_length=128):
        # Create a spectrogram from audio signals
        assert not np.iscomplexobj(samples), "You shall not pass in complex numbers"
        window = np.hanning(fft_length)[:, None]
        window_norm = np.sum(window**2)
        scale = window_norm * sample_rate
        trunc = (len(samples) - fft_length) % hop_length
        x = samples[: len(samples) - trunc]
        # Reshape to include the overlap
        nshape = (fft_length, (len(x) - fft_length) // hop_length + 1)
        nstrides = (x.strides[0], x.strides[0] * hop_length)
        x = as_strided(x, shape=nshape, strides=nstrides)
        # Window stride sanity check
        assert np.all(x[:, 1] == samples[hop_length : (hop_length + fft_length)])
        # Broadcast window, and then compute fft over columns and square mod
        x = np.fft.rfft(x * window, axis=0)
        x = np.absolute(x) ** 2
        # Scale 2.0 for everything except dc and fft_length/2
        x[1:-1, :] *= 2.0 / scale
        x[(0, -1), :] /= scale
        freqs = float(sample_rate) / fft_length * np.arange(x.shape[0])
        return x, freqs

    def spectrogram_from_file(
        self, filename, step=10, window=20, max_freq=None, eps=1e-14
    ):
        # Calculate log(linear spectrogram) from FFT energy
        with soundfile.SoundFile(filename) as sound_file:
            audio = sound_file.read(dtype="float32")
            sample_rate = sound_file.samplerate
            if audio.ndim >= 2:
                audio = np.mean(audio, 1)
            if max_freq is None:
                max_freq = sample_rate / 2
            if max_freq > sample_rate / 2:
                raise ValueError("max_freq can not be > than 0.5 of " " sample rate")
            if step > window:
                raise ValueError("step size can not be > than window size")
            hop_length = int(0.001 * step * sample_rate)
            fft_length = int(0.001 * window * sample_rate)
            pxx, freqs = self.spectrogramm(
                audio,
                fft_length=fft_length,
                sample_rate=sample_rate,
                hop_length=hop_length,
            )
            ind = np.where(freqs <= max_freq)[0][-1] + 1
        return np.transpose(np.log(pxx[:ind, :] + eps))

    def log_spectrogram_feature(
        self, samples, sample_rate, window_size=20, step_size=10, eps=1e-14
    ):
        nperseg = int(round(window_size * sample_rate / 1e3))
        noverlap = int(round(step_size * sample_rate / 1e3))
        freqs, times, spec = signal.spectrogram(
            samples,
            fs=sample_rate,
            window="hann",
            nperseg=nperseg,
            noverlap=noverlap,
            detrend=False,
        )
        freqs = freqs * 2
        return freqs, times, np.log(spec.T.astype(np.float64) + eps)

    def featurize(self, audio_clip):
        # Create features from data, either spectrogram or mfcc
        if self.spectrogram:
            return self.spectrogram_from_file(
                audio_clip, step=self.step, window=self.window, max_freq=self.max_freq
            )
        else:
            (rate, sig) = wav.read(audio_clip)
            return mfcc(sig, rate, numcep=self.mfcc_dim)

    def normalize(self, feature, eps=1e-14):
        # Scale the data to improve neural network performance and reduce the size of the gradients
        return (feature - self.feats_mean) / (self.feats_std + eps)

    # Custom CTC loss function (discussed below)
    def ctc_lambda_func(self, args):
        y_pred, labels, input_length, label_length = args
        return K.ctc_batch_cost(labels, y_pred, input_length, label_length)

    def add_ctc_loss(self, input_to_softmax):
        the_labels = Input(name="the_labels", shape=(None,), dtype="float32")
        input_lengths = Input(name="input_length", shape=(1,), dtype="int64")
        label_lengths = Input(name="label_length", shape=(1,), dtype="int64")
        output_lengths = Lambda(input_to_softmax.output_length)(input_lengths)
        # CTC loss is implemented in a lambda layer
        loss_out = Lambda(self.ctc_lambda_func, output_shape=(1,), name="ctc")(
            [input_to_softmax.output, the_labels, output_lengths, label_lengths]
        )
        model = Model(
            inputs=[input_to_softmax.input, the_labels, input_lengths, label_lengths],
            outputs=loss_out,
        )
        return model

    # Function for modifying CNN layers for sequence problems
    def cnn_output_length(
        self, input_length, filter_size, border_mode, stride, dilation=1
    ):
        # Compute the length of cnn output seq after 1D convolution across time
        if input_length is None:
            return None
        assert border_mode in {"same", "valid", "causal"}
        dilated_filter_size = filter_size + (filter_size - 1) * (dilation - 1)
        if border_mode == "same":
            output_length = input_length
        elif border_mode == "valid":
            output_length = input_length - dilated_filter_size + 1
        elif border_mode == "causal":
            output_length = input_length
        return (output_length + stride - 1) // stride

    def train_model(
        self,
        input_to_softmax,
        pickle_path,
        save_model_path,
        train_json="../data/train_corpus.json",
        valid_json="../data/valid_corpus.json",
        minibatch_size=16,  # You will want to change this depending on the GPU you are training on
        spectrogram=True,
        mfcc_dim=13,
        optimizer=Adam(
            lr=0.0001,
            beta_1=0.9,
            beta_2=0.999,
            epsilon=None,
            decay=0.0,
            amsgrad=False,
            clipnorm=1,
            clipvalue=0.5,
        ),
        epochs=30,  # You will want to change this depending on the model you are training and data you are using
        verbose=1,
        sort_by_duration=False,
        max_duration=10.0,
    ):

        # Obtain batches of data
        audio_gen = AudioGenerator(
            minibatch_size=minibatch_size,
            spectrogram=spectrogram,
            mfcc_dim=mfcc_dim,
            max_duration=max_duration,
            sort_by_duration=sort_by_duration,
        )
        # Load the datasets
        audio_gen.load_train_data(train_json)
        audio_gen.load_validation_data(valid_json)
        # Calculate steps per epoch
        num_train_examples = len(audio_gen.train_audio_paths)
        steps_per_epoch = num_train_examples // minibatch_size
        # Calculate validation steps
        num_valid_samples = len(audio_gen.valid_audio_paths)
        validation_steps = num_valid_samples // minibatch_size
        # Add custom CTC loss function to the nn
        model = self.add_ctc_loss(input_to_softmax)
        # Dummy lambda function for loss since CTC loss is implemented above
        model.compile(loss={"ctc": lambda y_true, y_pred: y_pred}, optimizer=optimizer)
        # Make  initial results/ directory for saving model pickles
        if not os.path.exists("../model"):
            os.makedirs("../model")
        # Add callbacks
        checkpointer = ModelCheckpoint(
            filepath="../model/" + save_model_path, verbose=0
        )
        terminator = callbacks.TerminateOnNaN()
        time_machiner = callbacks.History()
        logger = callbacks.CSVLogger("../logs/training.log")
        stopper = callbacks.EarlyStopping(
            monitor="val_loss", patience=2, verbose=1, mode="auto"
        )
        reducer = callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.1,
            patience=10,
            verbose=0,
            mode="auto",
            min_delta=0.0001,
            cooldown=0,
            min_lr=0,
        )
        tensor_boarder = callbacks.TensorBoard(
            log_dir="./logs",
            batch_size=16,
            write_graph=True,
            write_grads=True,
            write_images=True,
        )
        # Fit/train model
        hist = model.fit_generator(
            generator=audio_gen.next_train(),
            steps_per_epoch=steps_per_epoch,
            epochs=epochs,
            validation_data=audio_gen.next_valid(),
            validation_steps=validation_steps,
            callbacks=[
                checkpointer,
                terminator,
                logger,
                time_machiner,
                tensor_boarder,
                stopper,
                reducer,
            ],
            verbose=verbose,
        )
        # Save model loss
        with open("../model/" + pickle_path, "wb") as f:
            pickle.dump(hist.history, f)
