import random

from agent import Agent


class RandomAgent(Agent):
    def __init__(self):
        super().__init__(None)

    def getBestAction(self, ship, rocks):
        self.setInfo(ship, rocks)
        return random.randrange(0, 4)
