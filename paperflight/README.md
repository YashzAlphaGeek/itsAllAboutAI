# Paper Flight

A **2D Paper Flight Reinforcement Learning game** using **PPO (Proximal Policy Optimization)** in TensorFlow. The AI learns to throw a paper ball into a moving bin.

<img width="522" height="456" alt="image" src="https://github.com/user-attachments/assets/33bab92a-f75f-40fb-b0c5-01d291e6fe4e" />

---

## Project Structure

```
paperflight/
│
├── env/                 # Custom environment
│   └── paper_flight_env.py
│
├── server/              # Flask backend & trained model weights
│   ├── trained_actor.weights.h5
│   ├── trained_critic.weights.h5
│   └── app.py
│
├── static/              # Frontend JS, CSS
│   └── game.js
│
├── templates/           # HTML templates
│   └── index.html
│
├── train/               # Training scripts
│   └── train_ppo.py
│
├── PHYSICS.md           # Detailed physics explanation
│
└── README.md
```

---

## Installation

1. **Clone the repo**

```bash
git clone <your-repo-url>
cd paperflight
```

2. **Create a virtual environment**

```bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate # Linux/Mac
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

**`requirements.txt`**

```
tensorflow>=2.14
gymnasium
numpy
flask
flask-cors
```

---

## Usage

1. **Run the Flask server**

```bash
python server/app.py
```

2. **Open your browser**

```
http://127.0.0.1:5000/
```

The game should appear, and the AI will automatically throw the ball.

---

## Training the AI

The AI uses **PPO** to learn the optimal angle and power.

1. Edit hyperparameters in `train/train_ppo.py` (episodes, learning rates, etc.).
2. Run training:

```bash
python -m train.train_ppo
```

3. Trained weights are saved in `server/trained_actor.weights.h5` and `server/trained_critic.weights.h5`.

> **Note:** Frontend reads the `trained_actor.weights.h5` to throw balls automatically.

---

## Environment Details

* **State (`obs`)**: `[dx, dy, vx, vy]` normalized

  * `dx = (bin_x - ball_x) / canvas_width`
  * `dy = (ground_y - ball_y) / canvas_height`
  * `vx = ball velocity x / velocity scale`
  * `vy = ball velocity y / velocity scale`

* **Action**: `[angle, power]`

  * `angle` ∈ `[0.3, 1.0]` radians
  * `power` ∈ `[8, 12]` (pixels/frame)

* **Reward**

  * `+1` if ball lands in bin
  * `-0.5` otherwise

* **Physics**

  The ball moves under simple 2D physics (gravity, angle, power, and velocity). For a detailed, see [PHYSICS.md](PHYSICS.md).

---

## Frontend

* **Canvas:** `800x500` pixels
* **HUD:** Score, Angle, Power, Speed control
* **Trajectories:** Previous throws are shown with fading lines

---
