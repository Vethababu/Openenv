import random

class TrafficEnv:

    def __init__(self):
        self.reset()

    def reset(self):
        self.lane1 = 10
        self.lane2 = 10
        self.light = 0
        self.emergency = 0
        self.steps = 0

        return {
            "observation": self._obs()
        }

    def state(self):
        return {
            "observation": self._obs()
        }

    def step(self, action):

        # action 0 = keep
        # action 1 = switch
        if action == 1:
            self.light = 1 - self.light

        # traffic update
        if self.light == 0:
            self.lane1 = max(0, self.lane1 - 3)
            self.lane2 += random.randint(0, 2)
        else:
            self.lane2 = max(0, self.lane2 - 3)
            self.lane1 += random.randint(0, 2)

        # reward
        reward = -(self.lane1 + self.lane2)

        self.steps += 1
        done = self.steps >= 50

        return {
            "observation": self._obs(),
            "reward": reward,
            "done": done,
            "info": {}
        }

    def _obs(self):
        return {
            "lane1": self.lane1,
            "lane2": self.lane2,
            "light": self.light,
            "emergency": self.emergency
        }
