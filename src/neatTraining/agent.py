import pickle
import neat
import os

from calculations import *


class Agent:
    NUMBER_OF_ACTIONS = 4

    def __init__(self, net):
        self.net = net
        self.closestRock = None
        self.angleToClosestRock = None
        self.distanceToClosestRock = None
        self.vectorShipHeading = None

    def getBestAction(self, ship, rocks):
        self.setInfo(ship, rocks)

        inputs = (self.angleToClosestRock, self.distanceToClosestRock, ship.getTransformedAngle())
        outputs = self.net.activate(inputs)
        return outputs.index(max(outputs))

    def setInfo(self, ship, rocks):
        self.closestRock, self.distanceToClosestRock = getClosestRock(ship, rocks)
        self.angleToClosestRock, self.vectorShipHeading = getAngle(ship, self.closestRock)

    @staticmethod
    def loadFromFile(pathToNet, pathToConfig=None):
        if pathToConfig is None:
            folder = os.path.dirname(pathToNet)
            path_to_config = folder + "/neat-config"
        else:
            path_to_config = pathToConfig

        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                             neat.DefaultSpeciesSet, neat.DefaultStagnation,
                             path_to_config)
        net = neat.nn.FeedForwardNetwork.create(pickle.load(open(pathToNet, "rb")), config)
        return Agent(net)
