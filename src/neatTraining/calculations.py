import math
import numpy as np


def getClosestRock(ship, rocks):
    closest_rock = None
    min_distance = math.inf

    for rock in rocks:
        distance = getDistance(ship, rock)
        if distance < min_distance:
            closest_rock = rock
            min_distance = distance

    return closest_rock, distance


def getDistance(ship, rock):
    return math.sqrt(
        math.pow((rock.position.x - ship.position.x), 2) + math.pow((rock.position.y - ship.position.y), 2))


def getAngle(ship, rock):
    ship_tip = ship.transformedPointlist[0]
    # zielpunkt - startpunkt
    vector_to_rock_x = rock.position.x - ship_tip[0]
    vector_to_rock_y = rock.position.y - ship_tip[1]
    vector_to_rock = np.array([vector_to_rock_x, vector_to_rock_y])

    p1 = np.array(ship.transformedPointlist[2])
    p2 = np.array(ship.transformedPointlist[3])
    help = p2 - p1
    help2 = p1 + 0.5 * help
    vectorShipHeading = ship_tip - help2
    v1 = vectorShipHeading
    v2 = vector_to_rock
    return math.atan2(v1[0] * v2[1] - v1[1] * v2[0], v1[0] * v2[0] + v1[1] * v2[1]), vectorShipHeading


def _getMagnitude(vector):
    return np.sqrt(vector.dot(vector))
