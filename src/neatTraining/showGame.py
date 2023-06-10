from environment import Environment
from agent import Agent

agent = Agent.loadFromFile("winner.net")
env = Environment(True, windowed=True, debug=True)

ship, rocks, score, done = env.reset()
while not done:
    action = agent.getBestAction(ship, rocks)
    env.setDebugInfo(agent.closestRock, agent.vectorShipHeading, agent.angleToClosestRock, agent.distanceToClosestRock)
    ship, rocks, score, done = env.step(action)
