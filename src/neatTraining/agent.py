import pickle
import neat
import os
import random

from calculations import *


class Agent:
    NUMBER_OF_ACTIONS = 4
    ACTIONS = [0, 1, 2, 3]

    def __init__(self, net):
        self.net = net
        self.vectorShipHeading = None

        self.closestRock = None
        self.angleToClosestRock = None
        self.distanceToClosestRock = None

        self.closestRockOld = None
        self.angleToClosestRockOld = None
        self.distanceToClosestRockOld = None

        self.twoValuesPresent = False

    def getBestAction(self, ship, rocks):
        self.setInfo(ship, rocks)

        inputs = (self.angleToClosestRock, self.distanceToClosestRock, ship.getTransformedAngle(),
                  self.angleToClosestRockOld, self.distanceToClosestRockOld, int(self.twoValuesPresent))
        outputs = self.net.activate(inputs)

        result = []
        for i, output in enumerate(outputs):
            if output > 1:
                result.append(i)

        if 0 in result and 1 in result:
            output_left = outputs[0]
            output_right = outputs[1]

            if output_left > output_right:
                result.remove(1)
            elif output_left < output_right:
                result.remove(0)
            else:
                r = random.random()
                if r > 0.5:
                    result.remove(0)
                else:
                    result.remove(1)
        return result

    def setInfo(self, ship, rocks):
        self.closestRockOld = self.closestRock
        self.distanceToClosestRockOld = self.distanceToClosestRock
        self.closestRock, self.distanceToClosestRock = getClosestRock(ship, rocks)

        if self.closestRock is self.closestRockOld:
            self.twoValuesPresent = True
        else:
            self.twoValuesPresent = False

        self.angleToClosestRockOld = self.angleToClosestRock
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
