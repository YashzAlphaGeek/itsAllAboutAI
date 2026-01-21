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
print("Loaded weights from server/trained_actor.weights.h5")

def get_action(obs):
    obs = np.array(obs, dtype=np.float32).reshape(1, -1)
    mu = actor(obs).numpy()[0]


    bin_dist = obs[0][0]
    min_angle = 0.35
    max_angle = 1.0
    angle = min_angle + (max_angle - min_angle) * bin_dist
    angle += mu[0] * 0.2
    angle = np.clip(angle, min_angle, max_angle)

    min_power = 9
    max_power = 14
    power = min_power + (max_power - min_power) * bin_dist
    power += mu[1] * 1.0
    power = np.clip(power, min_power, max_power)

    print(f"Received obs: {obs[0]} | Returning action: {angle:.2f} {power:.2f}")
    return angle, power
