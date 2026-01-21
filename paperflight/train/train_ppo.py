import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
from env.paper_flight_env import PaperFlightEnv
import matplotlib.pyplot as plt

STATE_DIM = 4
ACTION_DIM = 2
GAMMA = 0.99
CLIP = 0.2
ACTOR_LR = 3e-4
CRITIC_LR = 1e-3
EPISODES = 500
THROWS_PER_EPISODE = 25
STD_START = 0.5
STD_END = 0.1
PPO_UPDATES = 6

env = PaperFlightEnv()

def build_actor():
    s = layers.Input((STATE_DIM,))
    x = layers.Dense(128, activation="relu")(s)
    x = layers.Dense(128, activation="relu")(x)
    mu = layers.Dense(ACTION_DIM, activation="tanh")(x)
    return tf.keras.Model(s, mu)

def build_critic():
    s = layers.Input((STATE_DIM,))
    x = layers.Dense(128, activation="relu")(s)
    x = layers.Dense(128, activation="relu")(x)
    v = layers.Dense(1)(x)
    return tf.keras.Model(s, v)

actor = build_actor()
critic = build_critic()
actor_opt = tf.keras.optimizers.Adam(ACTOR_LR)
critic_opt = tf.keras.optimizers.Adam(CRITIC_LR)

episode_list = []
reward_list = []
hits_list = []
near_hits_list = []

plt.ion()
fig, ax = plt.subplots(3, 1, figsize=(8, 8))

for ep in range(EPISODES):
    std = STD_START - (STD_START - STD_END) * (ep / EPISODES)

    states, actions, rewards, log_probs = [], [], [], []
    state = env.reset()
    total_reward = 0
    hits = 0
    near_hits = 0
    min_dist = float("inf")

    if ep < 1000:
        env.bin_x = 400 + np.random.rand() * 50

    for _ in range(THROWS_PER_EPISODE):
        mu = actor(state[None])
        action = mu + tf.random.normal(mu.shape) * std

        log_prob = -0.5 * tf.reduce_sum(
            ((action - mu) / std)**2 + 2*tf.math.log(std) + tf.math.log(2*np.pi),
            axis=1
        )

        angle = float(np.clip(mu[0, 0], 0.1, 1.2))
        power = float(np.clip(8 + (mu[0, 1] + 1) / 2 * 5, 8, 13))

        next_state, reward, done = env.step([angle, power])

        dist = abs(env.ball_x - env.bin_x)
        min_dist = min(min_dist, dist)

        if dist < 22:
            hits += 1
        elif dist < 50:
            near_hits += 1

        if dist < 22:
            shaped_reward = 5.0
        elif dist < 50:
            shaped_reward = 2.0
        else:
            shaped_reward = max(0, 1 - dist/300)
        reward = shaped_reward

        states.append(state)
        actions.append([angle, power])
        rewards.append(reward)
        log_probs.append(log_prob[0])
        total_reward += reward
        state = next_state

    returns = []
    G = 0
    for r in reversed(rewards):
        G = r + GAMMA * G
        returns.insert(0, G)
    returns = np.array(returns, dtype=np.float32)

    states = np.array(states, dtype=np.float32)
    actions = np.array(actions, dtype=np.float32)
    old_log_probs = tf.stack(log_probs)

    values = tf.squeeze(critic(states))
    advantages = returns - values.numpy()
    advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
    advantages = np.clip(advantages, -5.0, 5.0)

    for _ in range(PPO_UPDATES):
        with tf.GradientTape() as tape:
            mu = actor(states)
            new_log_probs = -0.5 * tf.reduce_sum(
                ((actions - mu)/std)**2 + 2*tf.math.log(std) + tf.math.log(2*np.pi),
                axis=1
            )
            ratio = tf.exp(new_log_probs - old_log_probs)
            clipped = tf.clip_by_value(ratio, 1 - CLIP, 1 + CLIP)
            actor_loss = -tf.reduce_mean(tf.minimum(ratio * advantages, clipped * advantages))
        grads = tape.gradient(actor_loss, actor.trainable_variables)
        actor_opt.apply_gradients(zip(grads, actor.trainable_variables))

    with tf.GradientTape() as tape:
        v = critic(states)
        critic_loss = tf.reduce_mean((returns - tf.squeeze(v))**2)
    grads = tape.gradient(critic_loss, critic.trainable_variables)
    critic_opt.apply_gradients(zip(grads, critic.trainable_variables))

    if ep % 25 == 0:
        print(f"EP {ep} | Total Reward: {total_reward:.2f} | Hits: {hits}/{THROWS_PER_EPISODE} | "
              f"Near Hits: {near_hits} | Min Dist: {min_dist:.2f} | STD: {std:.3f}")

    episode_list.append(ep)
    reward_list.append(total_reward)
    hits_list.append(hits)
    near_hits_list.append(near_hits)

    if ep % 25 == 0:
        ax[0].cla()
        ax[1].cla()
        ax[2].cla()

        ax[0].plot(episode_list, reward_list, label="Total Reward", color="blue")
        ax[0].legend()
        ax[1].plot(episode_list, hits_list, label="Hits", color="green")
        ax[1].legend()
        ax[2].plot(episode_list, near_hits_list, label="Near Hits", color="orange")
        ax[2].legend()
        plt.pause(0.01)

actor.save_weights("server/trained_actor.weights.h5")
critic.save_weights("server/trained_critic.weights.h5")
print("Training complete and weights saved")
plt.ioff()
plt.show()
