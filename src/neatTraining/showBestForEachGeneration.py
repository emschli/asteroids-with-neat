import os

from get_project_root import root_path
from environment import Environment
from agent import Agent

# Filenames to exclude
TO_EXCLUDE = ["winner.net", "avg_fitness.svg", "neat-config", "stats", "info"]

BASE_PATH = root_path(ignore_cwd=True) + "/resources/trainingResults/"
PATH = BASE_PATH + "v2_best/"

files = [file for file in os.listdir(PATH) if file not in TO_EXCLUDE]
generations = len(files)

env = Environment(True, windowed=True, debug=True, generationsMode=True)
env.setNumberOfGenerations(generations)

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
