import os

from get_project_root import root_path
from environment import Environment
from agent import Agent

BASE_PATH = root_path(ignore_cwd=True) + "/resources/trainingResults/"
PATH = BASE_PATH + "06|11|2023|15:15:34/"

env = Environment(True, windowed=True, debug=True, generationsMode=True)

generations = len(os.listdir(PATH)) - 3

for generation in range(generations):
    filename = str(generation) + ".net"
    agent = Agent.loadFromFile(PATH + filename)
    ship, rocks, score, done = env.reset()
    print("Showing Best of Generation " + str(generation))

    while True:
        action = agent.getBestAction(ship, rocks)
        env.setDebugInfo(agent.closestRock, agent.vectorShipHeading, agent.angleToClosestRock,
                         agent.distanceToClosestRock)

        ship, rocks, score, done = env.step(action)
        if done:
            break
