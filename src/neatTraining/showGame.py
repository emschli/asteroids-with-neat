from environment import Environment
from agent import Agent
from get_project_root import root_path
from readStats import getNameOfBestNetEver

BASE_PATH = root_path(ignore_cwd=True) + "/resources/trainingResults/"
RUN_FOLDER = "v2_best/"
NET_NAME = "winner.net"
# NET_NAME = getNameOfBestNetEver(BASE_PATH+RUN_FOLDER)

COMPLETE_PATH = BASE_PATH + RUN_FOLDER + NET_NAME

agent = Agent.loadFromFile(COMPLETE_PATH)
env = Environment(True, windowed=True, debug=True)

steps = 0
env.setSeed(1235)
ship, rocks, score, done = env.reset()
while not done:
    action = agent.getBestAction(ship, rocks)
    env.setDebugInfo(agent.closestRock, agent.vectorShipHeading, agent.angleToClosestRock, agent.distanceToClosestRock)
    ship, rocks, score, done = env.step(action)
    steps += 1

print("Steps: " + str(steps))
print("Score: " + str(score))
