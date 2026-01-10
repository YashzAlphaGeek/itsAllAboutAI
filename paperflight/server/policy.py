import numpy as np
import tensorflow as tf
from tensorflow.keras import layers

STATE_DIM = 4
ACTION_DIM = 2

def build_actor():
    s = layers.Input((STATE_DIM,))
    x = layers.Dense(128, activation="relu")(s)
    x = layers.Dense(128, activation="relu")(x)
    return tf.keras.Model(s, layers.Dense(ACTION_DIM, activation="tanh")(x))

actor = build_actor()
actor.load_weights("server/trained_actor.weights.h5")

def get_action(obs):
    obs = np.array(obs, dtype=np.float32).reshape(1, -1)
    mu = actor(obs).numpy()[0]

    # Tighter ranges for better control
    angle = float(np.clip(mu[0], 0.3, 1.0))
    power = float(np.clip(8 + (mu[1] + 1)/2 * 4, 8, 12))
    return angle, power
