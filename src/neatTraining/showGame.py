from environment import Environment
from agent import Agent

agent = Agent.loadFromFile("winner.net", "/home/mirjam/Nextcloud/Uni/S7/Evolutionäre Algorithmen/Prüfung/code/asteroids/src/neatTraining/neat-config")
env = Environment(True, windowed=True, debug=True)

steps = 0
ship, rocks, score, done = env.reset()
while not done:
    action = agent.getBestAction(ship, rocks)
    env.setDebugInfo(agent.closestRock, agent.vectorShipHeading, agent.angleToClosestRock, agent.distanceToClosestRock)
    ship, rocks, score, done = env.step(action)
    steps += 1

print("Steps: " + str(steps))
