import random

from agent import Agent


class RandomAgent(Agent):

    def __init__(self):
        super().__init__(None)

    def getBestAction(self, ship, rocks):
        self.setInfo(ship, rocks)
        random_size = random.randrange(0, 4)

        result = random.sample(self.ACTIONS, random_size)
        if 0 in result and 1 in result:
            r = random.random()
            if r > 0.5:
                result.remove(0)
            else:
                result.remove(1)
        return result
