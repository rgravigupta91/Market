import pandas as pd
import numpy as np
import tensorflow as tf

from sklearn.preprocessing      import MinMaxScaler
from tensorflow.keras.models    import Sequential, Model
from tensorflow.keras.layers    import LSTM, Dense, Dropout, Layer, LayerNormalization, MultiHeadAttention, Input, GlobalAveragePooling1D
from tensorflow.keras.callbacks import EarlyStopping

class PositionalEncoding(Layer):
    def __init__(self, sequence_len, d_model, **kwargs):
        super().__init__(**kwargs)
        self.sequence_len = sequence_len
        self.d_model = d_model

        pos = np.arange(sequence_len)[:, np.newaxis]
        i = np.arange(d_model)[np.newaxis, :]

        angle_rates = 1 / np.power(10000, (2*(i//2))/np.float32(d_model))
        angle_rads = pos * angle_rates

        angle_rads[:, 0::2] = np.sin(angle_rads[:, 0::2])
        angle_rads[:, 1::2] = np.cos(angle_rads[:, 1::2])

        self.pos_encoding = tf.constant(angle_rads[np.newaxis, ...], dtype=tf.float32)

    def call(self, inputs):
        return inputs + self.pos_encoding[:, :tf.shape(inputs)[1], :]

    def get_config(self):
        config = super().get_config()
        config.update({
            "sequence_len": self.sequence_len,
            "d_model": self.d_model
        })
        return config

class TransformerEncoder(tf.keras.layers.Layer):
    def __init__(self, embed_dim, num_heads, ff_dim, rate=0.1, **kwargs):
        super().__init__(**kwargs)
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.ff_dim = ff_dim
        self.rate = rate

        self.att = tf.keras.layers.MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim)
        self.ffn = tf.keras.Sequential([
            tf.keras.layers.Dense(ff_dim, activation="relu"),
            tf.keras.layers.Dense(embed_dim),
        ])
        self.layernorm1 = tf.keras.layers.LayerNormalization()
        self.layernorm2 = tf.keras.layers.LayerNormalization()
        self.dropout1 = tf.keras.layers.Dropout(rate)
        self.dropout2 = tf.keras.layers.Dropout(rate)

    def call(self, inputs, training=False):
        attn_output = self.att(inputs, inputs)
        attn_output = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(inputs + attn_output)

        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output, training=training)
        return self.layernorm2(out1 + ffn_output)

    def get_config(self):
        config = super().get_config()
        config.update({
            "embed_dim": self.embed_dim,
            "num_heads": self.num_heads,
            "ff_dim": self.ff_dim,
            "rate": self.rate
        })
        return config
      
""" class PositionalEncoding(Layer):
    def __init__(self, sequence_len, d_model):
        super().__init__()
        self.sequence_len = sequence_len
        self.d_model = d_model

    def call(self, x):
        position = tf.range(self.sequence_len, dtype=tf.float32)[:, tf.newaxis]
        div_term = tf.exp(
            tf.range(0, self.d_model, 2, dtype=tf.float32) *
            (-tf.math.log(10000.0) / self.d_model)
        )

        pe = tf.zeros((self.sequence_len, self.d_model))
        pe_even = tf.sin(position * div_term)
        pe_odd = tf.cos(position * div_term)

        pe = tf.reshape(
            tf.stack([pe_even, pe_odd], axis=2),
            (self.sequence_len, self.d_model)
        )

        pe = pe[tf.newaxis, ...]
        return x + pe[:, :tf.shape(x)[1], :]



class TransformerEncoder(Layer):
    def __init__(self, embed_dim, num_heads, ff_dim, rate=0.2):
        super().__init__()
        self.att = MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim)
        self.ffn = tf.keras.Sequential([
            Dense(ff_dim, activation="relu"),
            Dense(embed_dim),
        ])
        self.layernorm1 = LayerNormalization(epsilon=1e-6)
        self.layernorm2 = LayerNormalization(epsilon=1e-6)
        self.dropout1 = Dropout(rate)
        self.dropout2 = Dropout(rate)

    def call(self, inputs, training=False):
        attn_output = self.att(inputs, inputs)
        attn_output = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(inputs + attn_output)

        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output, training=training)
        return self.layernorm2(out1 + ffn_output)
"""

""" sequence_length = X_train.shape[1]
feature_dim = X_train.shape[2]
embed_dim = 64
num_heads = 4
ff_dim = 128

inputs = Input(shape=(sequence_length, feature_dim))
x = Dense(embed_dim)(inputs)
x = PositionalEncoding(sequence_length, embed_dim)(x)
x = TransformerEncoder(embed_dim, num_heads, ff_dim)(x)
x = Dropout(0.2)(x)
x = GlobalAveragePooling1D()(x)
x = Dense(16, activation="relu")(x)
outputs = Dense(1)(x)  # Regression output

model = Model(inputs=inputs, outputs=outputs)

model.compile(
    optimizer="adam",
    loss="mean_squared_error"
)

model.summary()




early_stop = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True
)

history = model.fit(
    X_train, y_train,
    epochs=100,
    batch_size=32,
    validation_split=0.1,
    callbacks=[early_stop],
    verbose=1
) """