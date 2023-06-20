import math
import numpy as np


def getClosestRock(ship, rocks):
    closest_rock = None
    min_distance = math.inf

    for rock in rocks:
        distance = getDistance(ship.position.asArray(), rock.position.asArray())
        if distance < min_distance:
            closest_rock = rock
            min_distance = distance

    return closest_rock, distance


def getDistance(x, y):
    return math.sqrt((y[0] - x[0])**2 + (y[1] - x[1])**2)
    # return math.sqrt(
    #     math.pow((rock.position.x - ship.position.x), 2) + math.pow((rock.position.y - ship.position.y), 2))


def getAngle(shipPointList, rock):
    ship_tip = shipPointList[0]
    vector_to_rock = getVectorBetween(ship_tip, rock.position.asArray())

    p1 = np.array(shipPointList[2])
    p2 = np.array(shipPointList[3])
    help_vector = p1 + 0.5 * getVectorBetween(p1, p2)
    vector_ship_heading = getVectorBetween(help_vector, ship_tip)

    return getAngleBetween(vector_ship_heading, vector_to_rock), vector_ship_heading


def getVectorBetween(x, y):
    x_value = y[0] - x[0]
    y_value = y[1] - x[1]
    return np.array([x_value, y_value])


def getAngleBetween(v1, v2):
    return math.atan2(v1[0] * v2[1] - v1[1] * v2[0], v1[0] * v2[0] + v1[1] * v2[1])


def _getMagnitude(vector):
    return np.sqrt(vector.dot(vector))
