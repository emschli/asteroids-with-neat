import neat
import statistics

from neat import ParallelEvaluator
root_path = "/home/jakob/Documents/asteroids-with-neat"
from datetime import datetime

from agent import Agent
from agentEvaluator import AgentEvaluator
from environment import Environment
from reporterForRandomness import ReporterForRandomness
from examples.visualize import *

SAVE_FOLDER = root_path + "/resources/trainingResults/"

RUNS_PER_CONFIG = 7
NUMBER_OF_GAMES = 5
GENERATIONS = 35
MAX_STEPS = 2_400

evaluator = AgentEvaluator(NUMBER_OF_GAMES, MAX_STEPS)

#
def fitness_function(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    agent = Agent(net)
    results = evaluator.evaluate(agent)
    return statistics.mean(results)


config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'neatTraining/neat-config')



import matplotlib.pyplot as plt

configurations = []
fitness_scores = []

# species_configs = [(0, 0, "no elitism"), (2, 0, "individual elitism"), (0, 1, "species elitism"), (2, 1, "both")] elitism, species_elitism, name
# [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
# [5,10,15,20,25,30,35,40,45,50,55,60,65]
# [0,10,20,30,40,50,60,70,80,90,100]
# [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
# [0.1, 1.0, 2.0, 3.0, 5.0, 10.0]
# [True, False]

for setting in [0.1, 1.0, 2.0, 3.0, 5.0, 10.0]:
    # config.reproduction_config.elitism = individual
    # config.stagnation_config.species_elitism = species
    # config.genome_config.conn_delete_prob = setting * 0.4
    # config.genome_config.conn_add_prob = setting
    # config.genome_config.node_add_prob = setting * 0.4
    # config.genome_config.node_delete_prob = setting
    # config.genome_config.weight_mutate_rate = setting
    # config.genome_config.weight_replace_rate = setting
    # config.genome_config.weight_mutate_power = setting
    # config.genome_config.bias_mutate_rate = setting
    # config.genome_config.conn_mutate_rate = setting
    # config.genome_config.bias_mutate_power = setting
    # config.genome_config.bias_replace_rate = setting
    # config.genome_config.feed_forward = setting
    # config.reproduction_config.survival_threshold = setting
    # config.stagnation.max_stagnation = setting
    config.species_set_config.compatibility_threshold = setting
    result = []
    # print(f'Testing {name}: elitism = {individual}, species_elitism = {species}')
    print(f'Testing setting {setting}:')

    for run in range(RUNS_PER_CONFIG):
        population = neat.Population(config)
        parallel = ParallelEvaluator(16, fitness_function)

        winner = population.run(parallel.evaluate, GENERATIONS)

        net = neat.nn.FeedForwardNetwork.create(winner, config)
        agent = Agent(net)
        run_result = statistics.mean(evaluator.evaluate(agent))

        print(f'    run result = {run_result}')

        result.append(run_result)

    configurations.append(setting)
    total_result = statistics.mean(result)
    print(f"=> Total result: {total_result}")
    fitness_scores.append(total_result)

import pickle as pkl



# Visualize the results
x = configurations
y = fitness_scores

file_x = open('params_x', 'ab')
pickle.dump(x,file_x)
file_x.close()
file_y = open('params_y', 'ab')
pickle.dump(y,file_y)
file_y.close()


fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlabel('Configuration')
ax.set_ylabel('Fitness Score')
ax.set_xticks(x)
ax.set_xticklabels(configurations)
ax.set_title('Fitness Scores for Different Configurations')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()