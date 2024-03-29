from environment import Environment
from randomAgent import RandomAgent

RENDERING = True
WINDOWED_MODE = True

agent = RandomAgent()
env = Environment(RENDERING, windowed=WINDOWED_MODE, debug=True)
ship, rocks, score, done = env.reset()

steps = 0
while not done:
    action = agent.getBestAction(ship, rocks)
    env.setDebugInfo(agent.closestRock, agent.vectorShipHeading, agent.angleToClosestRock, agent.distanceToClosestRock)
    ship, rocks, score, done = env.step(action)
    steps += 1

print("Final Score: " + str(score))
print("Steps: " + str(steps))
