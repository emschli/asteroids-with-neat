import random

from environment import Environment

NUMBER_OF_ACTIONS = 4
RENDERING = True

env = Environment(RENDERING)
ship, rocks, done = env.reset()

while not done:
    action = random.randrange(NUMBER_OF_ACTIONS)
    ship, rocks, done = env.step(action)
    env.render()
