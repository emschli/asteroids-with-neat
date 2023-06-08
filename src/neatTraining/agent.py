import random
import math
import numpy as np


class Agent:
    NUMBER_OF_ACTIONS = 4

    def __init__(self, net):
        self.net = net

    def getBestAction(self, ship, rocks):
        closest_rock, distance_to_closest_rock = self._getClosestRock(ship, rocks)
        angle_to_closest_rock = self._getAngle(ship, closest_rock)
        inputs = (angle_to_closest_rock, distance_to_closest_rock, ship.angle)
        outputs = self.net.activate(inputs)
        return outputs.index(max(outputs))
        # return random.randrange(self.NUMBER_OF_ACTIONS)

    def _getClosestRock(self, ship, rocks):
        closest_rock = None
        min_distance = math.inf

        for rock in rocks:
            distance = self._getDistanceEval(ship, rock)
            if distance < min_distance:
                closest_rock = rock
                min_distance = distance

        return closest_rock, distance

    def _getDistanceEval(self, ship, rock):
        return math.sqrt(math.pow((rock.position.x - ship.position.x), 2) + math.pow((rock.position.y - ship.position.y), 2))

    def _getAngle(self, ship, rock):
        ship_tip = ship.transformedPointlist[0]
        # zielpunkt - startpunkt
        vector_to_rock_x = rock.position.x - ship_tip.x
        vector_to_rock_y = rock.position.y - ship_tip.y

        vector_to_rock = np.array([vector_to_rock_x, vector_to_rock_y])
        vector_ship_heading = np.array([ship.heading.x, ship.heading.y])

        cross_product = np.cross(vector_ship_heading, vector_to_rock)
        return math.asin((self._getMagnitude(cross_product)) / (self._getMagnitude(vector_ship_heading) * self._getMagnitude(vector_to_rock)))

    def _getMagnitude(self, vector):
        return np.sqrt(vector.dot(vector))
