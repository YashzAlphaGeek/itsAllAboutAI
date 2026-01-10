import numpy as np
import tensorflow as tf
from tensorflow.keras import layers

STATE_DIM = 4
ACTION_DIM = 2

def build_actor():
    s = layers.Input((STATE_DIM,))
    x = layers.Dense(64, activation="relu")(s)
    x = layers.Dense(64, activation="relu")(x)
    return tf.keras.Model(s, layers.Dense(ACTION_DIM, activation="tanh")(x))

actor = build_actor()
actor.load_weights("server/trained_actor.weights.h5")

def get_action(obs):
    obs = np.array(obs, dtype=np.float32).reshape(1, -1)

    mu = actor(obs).numpy()[0]

    angle = float(np.clip(mu[0], 0.3, 1.0))
    min_power = 8.0
    max_power = 12.0
    raw_power = 8 + (mu[1] + 1) / 2 * 8
    power = float(np.clip(raw_power, min_power, max_power))

    return angle, power
