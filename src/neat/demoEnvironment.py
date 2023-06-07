from environment import Environment
from agent import Agent

RENDERING = False
WINDOWED_MODE = True

agent = Agent()
env = Environment(RENDERING, windowed=WINDOWED_MODE)
ship, rocks, score, done = env.reset()

while not done:
    action = agent.getBestAction(ship, rocks)
    ship, rocks, score, done = env.step(action)

print("Final Score: " + str(score))
