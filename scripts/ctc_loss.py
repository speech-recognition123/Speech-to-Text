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
import os, sys
sys.path.insert(0, '../scripts/')
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
import tensorflow as tf
import os, sys
sys.path.insert(0, '../scripts/')
sys.path.append(os.path.abspath(os.path.join('..')))
from keras.layers import Input, Lambda, Dense, Dropout, Flatten, Embedding, Activation, GRUCell, LSTMCell,SimpleRNNCell

class CTC_loss:

    def __init__(self, hop_size):
        self.hop_size = hop_size

    def ctc_lambda_func(self, args):
        y_pred, labels, input_length, label_length = args
        return K.ctc_batch_cost(labels, y_pred, input_length, label_length)

    def input_lengths_lambda_func(self, args):
        hop_size = self.hop_size
        input_length = args
        return tf.cast(tf.math.ceil(input_length/hop_size)-1, dtype="float32")

    def add_ctc_loss(self, model_builder):
        the_labels = Input(name='the_labels',
                           shape=(None,), dtype='float32')
        input_lengths = Input(name='input_length',
                              shape=(1,), dtype='float32')
        label_lengths = Input(name='label_length',
                              shape=(1,), dtype='float32')

        input_lengths2 = Lambda(self.input_lengths_lambda_func)(input_lengths)

        if model_builder.output_length:
            output_lengths = Lambda(
                model_builder.output_length)(input_lengths2)
        else:
            output_lengths = input_lengths2

        loss_out = Lambda(self.ctc_lambda_func, output_shape=(1,), name='ctc')(
            [model_builder.output, the_labels, output_lengths, label_lengths])
        model = Model(inputs=[model_builder.input, the_labels,
                      input_lengths, label_lengths],  outputs=loss_out)
        return model
    