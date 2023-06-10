import neat
import statistics
import pickle

from neat import ParallelEvaluator

from neatTraining.agent import Agent
from neatTraining.agentEvaluator import AgentEvaluator
from neatTraining.environment import Environment
from reporterForRandomness import ReporterForRandomness

NUMBER_OF_GAMES = 5
GENERATIONS = 100
MAX_STEPS = 1_000_000

evaluator = AgentEvaluator(NUMBER_OF_GAMES, MAX_STEPS)


def fitness_function(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    agent = Agent(net)
    results = evaluator.evaluate(agent)
    return statistics.mean(results)


def fitness_function_not_parallel(genomes, config):
    evaluator = config.evaluator

    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        agent = Agent(net)
        results = evaluator.evaluate(agent)
        genome.fitness = statistics.mean(results)

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'neat-config')


population = neat.Population(config)
parallel = ParallelEvaluator(16, fitness_function)
population.add_reporter(neat.StdOutReporter(False))
population.add_reporter(ReporterForRandomness(evaluator))

winner = population.run(parallel.evaluate, GENERATIONS)
# winner = population.run(fitness_function_not_parallel, GENERATIONS)

net = neat.nn.FeedForwardNetwork.create(winner, config)
agent = Agent(net)

env = Environment(True, windowed=True)
ship, rocks, score, done = env.reset()

while not done:
    action = agent.getBestAction(ship, rocks)
    ship, rocks, score, done = env.step(action)

print("Final Score: " + str(score))

pickle.dump(winner, open("winner.net", "wb"))
