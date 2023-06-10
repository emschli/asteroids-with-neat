import pickle
import neat

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
    def loadFromFile(pathToFile):
        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                             neat.DefaultSpeciesSet, neat.DefaultStagnation,
                             'neat-config')
        net = neat.nn.FeedForwardNetwork.create(pickle.load(open(pathToFile, "rb")), config)
        return Agent(net)
