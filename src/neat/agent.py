import random


class Agent:
    NUMBER_OF_ACTIONS = 4

    def getBestAction(self, ship, rocks):
        return random.randrange(self.NUMBER_OF_ACTIONS)
