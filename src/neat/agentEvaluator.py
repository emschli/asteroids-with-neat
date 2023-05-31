from environment import Environment


class AgentEvaluator:
    def __init__(self):
        self.env = Environment(False)

    def evaluate(self, agent, numberOfGames):
        scores = []
        for i in range(numberOfGames):
            ship, rocks, score, done = self.env.reset()

            while not done:
                action = agent.getBestAction(ship, rocks)
                ship, rocks, score, done = self.env.step(action)

            scores.append(score)

        return scores


if __name__ == "__main__":
    from agent import Agent
    import statistics

    num_of_games = 100
    agent = Agent()
    evaluator = AgentEvaluator()
    results = evaluator.evaluate(agent, num_of_games)
    mean = statistics.mean(results)
    print("Random Agent got Mean Score of " + str(mean) + " over " + str(num_of_games) + " Games")
