import random

from environment import Environment

NUMBER_OF_ACTIONS = 4
RENDERING = False
WINDOWED_MODE = True

env = Environment(RENDERING, WINDOWED_MODE)
ship, rocks, done = env.reset()

while not done:
    action = random.randrange(NUMBER_OF_ACTIONS)
    ship, rocks, score, done = env.step(action)

print("Final Score: " + str(score))
