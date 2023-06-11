import neat
import statistics
import pickle
import os
import shutil

from neat import ParallelEvaluator
from get_project_root import root_path
from datetime import datetime

from neatTraining.agent import Agent
from neatTraining.agentEvaluator import AgentEvaluator
from neatTraining.environment import Environment
from reporterForRandomness import ReporterForRandomness

SAVE_FOLDER = root_path(ignore_cwd=True) + "/resources/trainingResults/"

NUMBER_OF_GAMES = 1
GENERATIONS = 100
MAX_STEPS = 30_000

evaluator = AgentEvaluator(NUMBER_OF_GAMES, MAX_STEPS)
timestamp = datetime.now().strftime("%m|%d|%Y|%H:%M:%S")
folder = SAVE_FOLDER + timestamp
os.mkdir(folder)


def fitness_function(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    agent = Agent(net)
    results = evaluator.evaluate(agent)
    return statistics.mean(results)


config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'neat-config')

shutil.copy('neat-config', folder + '/neat-config')


population = neat.Population(config)
parallel = ParallelEvaluator(16, fitness_function)
population.add_reporter(neat.StdOutReporter(False))
population.add_reporter(ReporterForRandomness(evaluator, folder))
stats = neat.StatisticsReporter()
population.add_reporter(stats)

winner = population.run(parallel.evaluate, GENERATIONS)

# Evolution Done
net = neat.nn.FeedForwardNetwork.create(winner, config)
agent = Agent(net)

env = Environment(True, windowed=True)
ship, rocks, score, done = env.reset()

while not done:
    action = agent.getBestAction(ship, rocks)
    ship, rocks, score, done = env.step(action)

print("Final Score: " + str(score))

pickle.dump(winner, open(folder + "/winner.net", "wb"))
pickle.dump(stats, open(folder + "/stats", "wb"))
