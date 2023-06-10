import random

from environment import Environment


class AgentEvaluator:

    def __init__(self, numberOfGames):
        self.env = Environment(False)
        self.numberOfGames = numberOfGames
        self.seeds = []
        self.generateSeeds()

    def generateSeeds(self):
        self.seeds = [random.randint(0, 1000) for _ in range(0, self.numberOfGames)]

    def evaluate(self, agent):
        scores = []
        for i in range(self.numberOfGames):
            self.env.setSeed(self.seeds[i])
            ship, rocks, score, done = self.env.reset()

            while not done:
                action = agent.getBestAction(ship, rocks)
                ship, rocks, score, done = self.env.step(action)

            scores.append(score)

        return scores
