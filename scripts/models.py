import tensorflow as tf
from tensorflow.keras.layers import *
from tensorflow.keras.models import Model

from .logspectrogram import LogMelSpectrogram


def build_model(
    output_dim,
    cnn_model,
    custom_model,
    preprocess_model,
    mfcc=False,
    calc=None,
):
    input_audios = Input(name="the_input", shape=(None,))
    pre = preprocess_model(input_audios)
    pre = tf.squeeze(pre, [3])
    cnn_output = cnn_model(pre)
    y_pred = custom_model(cnn_output)
    model = Model(inputs=input_audios, outputs=y_pred, name="model_builder")
    model.output_length = calc

    return model


def cnn_net(n_mels):
    input_data = Input(name="the_input", shape=(None, n_mels, 1))
    y = Conv2D(128, (7, 7), padding="same")(input_data)  # was 32
    y = Activation("relu")(y)
    y = BatchNormalization()(y)
    y = MaxPooling2D((1, 2))(y)
    y = Conv2D(64, (5, 5), padding="same")(y)  # was 32
    y = Activation("relu")(y)
    y = BatchNormalization()(y)
    y = MaxPooling2D((1, 2))(y)
    y = Conv2D(64, (3, 3), padding="same")(y)  # was 32
    y = Activation("relu")(y)
    y = BatchNormalization()(y)
    y = MaxPooling2D((1, 2))(y)
    y = Reshape((-1, y.shape[-1] * y.shape[-2]))(y)

    model = Model(inputs=input_data, outputs=y, name="cnn_net")
    return model, model.output.shape


def bi_directional_rnn(
    input_dim,
    batch_size,
    sample_rate=8000,
    rnn_layers=4,
    units=400,
    drop_out=0.5,
    act="tanh",
    output_dim=224,
):
    input_data = Input(name="the_input", shape=(None, input_dim))
    x = Bidirectional(
        LSTM(units, activation=act, return_sequences=True, implementation=2)
    )(input_data)
    x = BatchNormalization()(x)
    x = Dropout(drop_out)(x)

    for i in range(rnn_layers - 2):
        x = Bidirectional(LSTM(units, activation=act, return_sequences=True))(
            x
        )
        x = BatchNormalization()(x)
        x = Dropout(drop_out)(x)

    x = Bidirectional(
        LSTM(units, activation=act, return_sequences=True, implementation=2)
    )(x)
    x = BatchNormalization()(x)
    x = Dropout(drop_out)(x)

    time_dense = TimeDistributed(Dense(output_dim))(x)
    y_pred = Activation("softmax", name="softmax")(time_dense)
    model = Model(inputs=input_data, outputs=y_pred, name="bi_directional_rnn")

    return model


def preprocess_model(sample_rate, fft_size, frame_step, n_mels, mfcc=False):
    input_data = Input(name="input", shape=(None,), dtype="float32")
    feat_layer = LogMelSpectrogram(
        fft_size=fft_size,
        hop_size=frame_step,
        n_mels=n_mels,
        sample_rate=sample_rate,
        f_min=0.0,
        f_max=int(sample_rate / 2),
    )(input_data)

    x = BatchNormalization(axis=2)(feat_layer)
    model = Model(inputs=input_data, outputs=x, name="preprocess_model")

    return model
