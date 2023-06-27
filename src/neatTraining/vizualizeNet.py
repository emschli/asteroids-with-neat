from get_project_root import root_path
from neat import DefaultGenome
from neat.graphs import required_for_output
import neat

from examples.visualize import draw_net
import neat
import pickle
import copy

from readStats import getNameOfBestNetEver


def getSampleStartingGenome(config, key=1):
    population = neat.Population(config)
    return population.population[key]


def get_pruned_copy(genome, genome_config):
    used_node_genes, used_connection_genes = get_pruned_genes(genome.nodes, genome.connections,
                                                              genome_config.input_keys, genome_config.output_keys)
    new_genome = DefaultGenome(None)
    new_genome.nodes = used_node_genes
    new_genome.connections = used_connection_genes
    return new_genome


def get_pruned_genes(node_genes, connection_genes, input_keys, output_keys):
    used_nodes = required_for_output(input_keys, output_keys, connection_genes)
    used_pins = used_nodes.union(input_keys)

    # Copy used nodes into a new genome.
    used_node_genes = {}
    for n in used_nodes:
        used_node_genes[n] = copy.deepcopy(node_genes[n])

    # Copy enabled and used connections into the new genome.
    used_connection_genes = {}
    for key, cg in connection_genes.items():
        in_node_id, out_node_id = key
        if cg.enabled and in_node_id in used_pins and out_node_id in used_pins:
            used_connection_genes[key] = copy.deepcopy(cg)

    return used_node_genes, used_connection_genes


BASE_PATH = root_path(ignore_cwd=True) + "/resources/trainingResults/"
RUN_FOLDER = "v5_final/"
# NET_NAME = "winner.net"
NET_NAME = getNameOfBestNetEver(BASE_PATH + RUN_FOLDER)

COMPLETE_PATH = BASE_PATH + RUN_FOLDER + NET_NAME
PATH_TO_CONFIG = BASE_PATH + RUN_FOLDER + "neat-config"
GRAPH_FILE = BASE_PATH + RUN_FOLDER + "graph"
genome = pickle.load(open(COMPLETE_PATH, "rb"))

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                             neat.DefaultSpeciesSet, neat.DefaultStagnation,
                             PATH_TO_CONFIG)

node_names_min_config = {
    -1: 'angle closest rock',
    -2: 'distance closest rock',
    -3: 'angle ship',
    # -4: 'MIDDLE LEFT',
    # -5: 'MIDDLE RIGHT',
    # -6: 'bottom left',
    # -7: 'BOTTOM MIDDLE',
    # -8: 'bottom right',
    0: 'LEFT',
    1: 'RIGHT',
    2: 'DASH',
    3: 'FIRE'
    }

node_names_two_frames = {
    -1: 'angle closest rock',
    -2: 'distance closest rock',
    # -3: 'angle diff',
    # -4: 'distance diff',
    -3: 'angle ship',
    -4: 'angle closest rock (OLD)',
    -5: 'distance closest rock (OLD)',
    -6: 'angle ship (OLD)',
    -7: 'two valid values',
    -8: 'can shoot',
    0: 'LEFT',
    1: 'RIGHT',
    2: 'DASH',
    3: 'FIRE'
    }

pruned_genome = get_pruned_copy(genome, config.genome_config)
draw_net(config, pruned_genome, True, node_names=node_names_two_frames, show_disabled=False, filename=GRAPH_FILE)

# min_config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
#                              neat.DefaultSpeciesSet, neat.DefaultStagnation,
#                              "/home/mirjam/Nextcloud/Uni/S7/Evolutionäre Algorithmen/Prüfung/code/asteroids/resources/trainingResults/v2_best/neat-config")
#
# starting_genome = getSampleStartingGenome(min_config)
# pruned_starting_genome = get_pruned_copy(starting_genome, min_config.genome_config)
# draw_net(min_config, pruned_starting_genome, True, node_names=node_names_min_config, show_disabled=False, filename="min")

