import neat

from neatTraining.agent  import Agent


def evaluation_function(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    evaluator = config.evaluator
    agent = Agent()