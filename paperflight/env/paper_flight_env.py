import numpy as np

class PaperFlightEnv:
    def __init__(self):
        self.ground_y = 430
        self.dt = 0.25
        self.vscale = 12.0
        self.reset()

    def reset(self):
        self.ball_x = 100
        self.ball_y = self.ground_y
        self.vx = 0
        self.vy = 0
        self.bin_x = 200 + np.random.rand() * 400
        return self._get_state()

    def _get_state(self):
        return np.array([
            (self.bin_x - self.ball_x) / 800,
            (self.ground_y - self.ball_y) / 600,
            self.vx / self.vscale,
            self.vy / self.vscale
        ], dtype=np.float32)

    def step(self, action):
        angle, power = action
        self.vx = np.cos(angle) * power
        self.vy = -np.sin(angle) * power

        self.ball_x += self.vx * self.dt
        self.ball_y += self.vy * self.dt
        self.vy += 0.25  # gravity

        done = self.ball_y >= self.ground_y
        reward = 0.0
        if done:
            dist = abs(self.ball_x - self.bin_x)
            ## reward = 1.0 if dist < 22 else -0.5
            reward = 1.0 if dist < 22 else 1 - min(dist / 800, 1.0)

        return self._get_state(), reward, done
