import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
from env.paper_flight_env import PaperFlightEnv

# --------------------
# Hyperparameters
# --------------------
STATE_DIM = 4
ACTION_DIM = 2
GAMMA = 0.99
CLIP = 0.2
ACTOR_LR = 3e-4
CRITIC_LR = 1e-3
EPISODES = 2000
THROWS_PER_EPISODE = 10
STD = 0.15

# --------------------
# Environment
# --------------------
env = PaperFlightEnv()

# --------------------
# Actor & Critic Networks
# --------------------
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

# --------------------
# Training Loop
# --------------------
for ep in range(EPISODES):
    states, actions, rewards, log_probs = [], [], [], []
    state = env.reset()
    total_reward = 0

    for _ in range(THROWS_PER_EPISODE):
        mu = actor(state[None])
        std = tf.ones_like(mu) * STD
        action = mu + tf.random.normal(mu.shape) * std

        log_prob = -0.5 * tf.reduce_sum(
            ((action - mu) / std)**2 + 2*tf.math.log(std) + tf.math.log(2*np.pi),
            axis=1
        )

        # Clip & map actions
        angle = float(np.clip(action[0,0], 0.3, 1.0))
        power = float(np.clip(8 + (action[0,1] + 1)/2 * 4, 8, 12))

        next_state, reward, done = env.step([angle, power])

        states.append(state)
        actions.append([angle, power])
        rewards.append(reward)
        log_probs.append(log_prob[0])

        total_reward += reward
        state = next_state

    # Compute discounted returns
    returns = []
    G = 0
    for r in reversed(rewards):
        G = r + GAMMA * G
        returns.insert(0, G)
    returns = np.array(returns, dtype=np.float32)

    states = np.array(states, dtype=np.float32)
    actions = np.array(actions, dtype=np.float32)
    old_log_probs = tf.stack(log_probs)

    # Advantages
    values = tf.squeeze(critic(states))
    advantages = returns - values.numpy()
    advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
    advantages = np.clip(advantages, -5.0, 5.0)

    # PPO actor update
    for _ in range(4):
        with tf.GradientTape() as tape:
            mu = actor(states)
            std = tf.ones_like(mu) * STD
            new_log_probs = -0.5 * tf.reduce_sum(
                ((actions - mu)/std)**2 + 2*tf.math.log(std) + tf.math.log(2*np.pi),
                axis=1
            )
            ratio = tf.exp(new_log_probs - old_log_probs)
            clipped = tf.clip_by_value(ratio, 1 - CLIP, 1 + CLIP)
            actor_loss = -tf.reduce_mean(tf.minimum(ratio * advantages, clipped * advantages))
        grads = tape.gradient(actor_loss, actor.trainable_variables)
        actor_opt.apply_gradients(zip(grads, actor.trainable_variables))

    # Critic update
    with tf.GradientTape() as tape:
        v = critic(states)
        critic_loss = tf.reduce_mean((returns - tf.squeeze(v))**2)
    grads = tape.gradient(critic_loss, critic.trainable_variables)
    critic_opt.apply_gradients(zip(grads, critic.trainable_variables))

    if ep % 25 == 0:
        print(f"EP {ep} | Total Reward: {total_reward:.2f}")

# Save weights
actor.save_weights("server/trained_actor.weights.h5")
critic.save_weights("server/trained_critic.weights.h5")
print("✅ Training complete and weights saved")
