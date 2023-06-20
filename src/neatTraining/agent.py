import math
import pickle
import neat
import os
import random

from calculations import *
from environment import Environment
import copy


class Agent:
    NUMBER_OF_ACTIONS = 4
    ACTIONS = [0, 1, 2, 3]

    MAX_DISTANCE = math.sqrt(Environment.WIDTH**2 + Environment.HEIGHT**2)

    def __init__(self, net):
        self.net = net
        self.vectorShipHeading = None
        self.oldShipPointList = None

        self.closestRock = None
        self.angleToClosestRock = None
        self.distanceToClosestRock = None

        # Movement Info
        self.angleDiff = None
        self.distanceDiff = None
        self.futureAngle = None

        self.closestRockOld = None
        self.angleToClosestRockOld = None
        self.distanceToClosestRockOld = None

        self.twoValuesPresent = False
        self.shipAngle = None
        self.oldShipAngle = None

    def getBestAction(self, ship, rocks):
        self.setInfo(ship, rocks)

        can_shoot = len(ship.bullets) < ship.maxBullets

        inputs = (self.angleToClosestRock,
                  self.distanceToClosestRock / self.MAX_DISTANCE,
                  # self.shipAngle,
                  # self.angleToClosestRockOld,
                  # self.distanceToClosestRockOld / self.MAX_DISTANCE,
                  # self.oldShipAngle,
                  # self.angleDiff,
                  # self.distanceDiff / self.MAX_DISTANCE,
                  # self.futureAngle,
                  # float(self.twoValuesPresent),
                  # float(can_shoot)
                  )
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
        self.oldShipPointList = copy.deepcopy(ship.transformedPointlist)
        self.oldShipAngle = self.shipAngle
        self.shipAngle = ship.getTransformedAngle()

        self.closestRockOld = self.closestRock
        self.distanceToClosestRockOld = self.distanceToClosestRock
        self.closestRock, self.distanceToClosestRock = getClosestRock(ship, rocks)

        self.angleToClosestRockOld = self.angleToClosestRock
        self.angleToClosestRock, self.vectorShipHeading = getAngle(ship.transformedPointlist, self.closestRock)

        if self.closestRock is self.closestRockOld:
            self.twoValuesPresent = True
            new_angle, _ = getAngle(self.oldShipPointList, self.closestRock)
            self.angleDiff = new_angle - self.angleToClosestRockOld
            new_distance = getDistance(self.oldShipPointList[0], self.closestRock.position.asArray())
            self.distanceDiff = self.distanceToClosestRockOld - new_distance
        else:
            self.twoValuesPresent = False
            self.angleDiff = 0.0
            self.distanceDiff = 0.0

        self.futureAngle, _ = getAngle(ship.transformedPointlist, self.closestRock.getFutureRock())

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
