from environment import Environment
from randomAgent import RandomAgent

RENDERING = True
WINDOWED_MODE = True

agent = RandomAgent()
env = Environment(RENDERING, windowed=WINDOWED_MODE, debug=True)
ship, rocks, score, done = env.reset()

while not done:
    action = agent.getBestAction(ship, rocks)
    env.setDebugInfo(agent.closestRock, agent.vectorShipHeading, agent.angleToClosestRock, agent.distanceToClosestRock)
    ship, rocks, score, done = env.step(action)

print("Final Score: " + str(score))
