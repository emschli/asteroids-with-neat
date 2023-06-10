import random

from environment import Environment


class AgentEvaluator:

    def __init__(self, numberOfGames, maxSteps):
        self.env = Environment(False)
        self.numberOfGames = numberOfGames
        self.seeds = []
        self.generateSeeds()
        self.maxSteps = maxSteps

    def generateSeeds(self):
        self.seeds = [random.randint(0, 1000) for _ in range(0, self.numberOfGames)]

    def evaluate(self, agent):
        scores = []
        for i in range(self.numberOfGames):
            self.env.setSeed(self.seeds[i])
            ship, rocks, score, done = self.env.reset()

            steps = 0
            while not done and steps < self.maxSteps:
                action = agent.getBestAction(ship, rocks)
                ship, rocks, score, done = self.env.step(action)
                steps += 1

            scores.append(score)

        return scores
