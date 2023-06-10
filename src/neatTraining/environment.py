import math
import random
import sys

import numpy
import pygame
from pygame.locals import *

from badies import Rock, Debris
from ship import Ship
from stage import Stage
from util.vector2d import Vector2d


class WrongActionException(Exception):
    pass


class Environment:
    WIDTH = 1024
    HEIGHT = 768
    GAME_SPEED = 10

    RED = (255, 0, 0)
    WHITE = (255, 255, 255)

    def __init__(self, rendering, seed=42, windowed=True, debug=False):
        self.rendering = rendering
        self.stage = Stage(rendering, windowed, 'Atari Asteroids', (self.WIDTH, self.HEIGHT))
        self.seed = seed

        self.numRocks = 3
        self.rockList = []
        self.score = 0
        self.ship = None
        self.lives = 1

        if rendering:
            self.clock = pygame.time.Clock()
            self.debug = debug

    def reset(self):
        random.seed(self.seed)
        self.initialiseGame()
        return self.ship, self.rockList, self.score, False

    # 0 -> left, 1 -> right, 2 -> dash, 3 -> fire
    def step(self, action):
        self.processInput(action)

        self.stage.moveSprites()

        self.checkCollisions()

        done = self.lives <= 0

        if len(self.rockList) == 0:
            self.levelUp()

        self.render()

        return self.ship, self.rockList, self.score, done

    def setSeed(self, seed):
        self.seed = seed

    def setDebugInfo(self, closestRock, directionOfShip, angle, distanceToClosestRock):
        self.closestRock = closestRock
        self.directionOfShip = directionOfShip
        self.angle = angle
        self.distanceToClosestRock = distanceToClosestRock

    def drawDebugInfo(self):
        for rock in self.rockList:
            if rock is self.closestRock:
                rock.color = self.RED
            else:
                rock.color = self.WHITE

        ship_tip = self.ship.transformedPointlist[0]
        self.stage.drawLine(ship_tip, (self.closestRock.position.x, self.closestRock.position.y))

        direction = numpy.array(ship_tip) + numpy.array(self.directionOfShip)
        self.stage.drawLine(ship_tip, direction)

        #show angleText
        font1 = pygame.font.SysFont('arial', 10)
        angleStr = str("{:10.2f}".format(self.angle / math.pi))
        angleText = font1.render(angleStr, True, self.RED)
        x = ship_tip[0] + 20
        y = ship_tip[1]
        scoreTextRect = angleText.get_rect(centerx=x, centery=y)
        self.stage.screen.blit(angleText, scoreTextRect)
         # show ship angle
        font1 = pygame.font.SysFont('arial', 10)
        angleStr = str("{:10.2f}".format(self.ship.getTransformedAngle() / math.pi))
        # angleStr = str("{:10.2f}".format(self.distanceToClosestRock))
        angleText = font1.render(angleStr, True, self.RED)
        x = self.ship.position.x - 10
        y = self.ship.position.y
        scoreTextRect = angleText.get_rect(centerx=x, centery=y)
        self.stage.screen.blit(angleText, scoreTextRect)

    def render(self):
        if self.rendering:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        sys.exit(0)
                else:
                    pass
            self.clock.tick(self.GAME_SPEED)
            self.stage.screen.fill((10, 10, 10))
            self.stage.drawSprites()
            if self.debug:
                self.drawDebugInfo()
            self.displayScore()
            pygame.display.flip()
        else:
            self.stage.drawSprites()

    def initialiseGame(self):
        [self.stage.removeSprite(sprite)
         for sprite in self.rockList]

        self.createNewShip()
        self.score = 0
        self.rockList = []
        self.numRocks = 3
        self.createRocks(self.numRocks)
        self.lives = 1

    def createRocks(self, numRocks):
        for _ in range(0, numRocks):
            position = Vector2d(random.randrange(-10, 10),
                                random.randrange(-10, 10))
            newRock = Rock(position, Rock.largeRockType)

            self.stage.addSprite(newRock)
            self.rockList.append(newRock)

    def createNewShip(self):
        if self.ship:
            [self.stage.spriteList.remove(debris)
             for debris in self.ship.shipDebrisList]
        self.ship = Ship(self.stage)
        self.stage.addSprite(self.ship.thrustJet)
        self.stage.addSprite(self.ship)

    def processInput(self, action):
        self.ship.thrustJet.accelerating = False

        if action == 3:
            self.ship.fireBullet()
        elif action == 2:
            self.ship.increaseThrust()
            self.ship.thrustJet.accelerating = True
        elif action == 1:
            self.ship.rotateRight()
        elif action == 0:
            self.ship.rotateLeft()
        else:
            raise WrongActionException

    def checkCollisions(self):
        # Ship bullet hit rock?
        shipHit = False

        # Rocks
        for rock in self.rockList:
            rockHit = False

            if not self.ship.inHyperSpace and rock.collidesWith(self.ship):
                p = rock.checkPolygonCollision(self.ship)
                if p is not None:
                    shipHit = True
                    rockHit = True

            if self.ship.bulletCollision(rock):
                rockHit = True

            if rockHit:
                self.rockList.remove(rock)
                self.stage.spriteList.remove(rock)

                if rock.rockType == Rock.largeRockType:
                    # playSound("explode1")
                    newRockType = Rock.mediumRockType
                    self.score += 50
                elif rock.rockType == Rock.mediumRockType:
                    # playSound("explode2")
                    newRockType = Rock.smallRockType
                    self.score += 100
                else:
                    # playSound("explode3")
                    self.score += 200

                if rock.rockType != Rock.smallRockType:
                    # new rocks
                    for _ in range(0, 2):
                        position = Vector2d(rock.position.x, rock.position.y)
                        newRock = Rock(position, newRockType)
                        self.stage.addSprite(newRock)
                        self.rockList.append(newRock)

                self.createDebris(rock)

        if shipHit:
            self.killShip()

            # comment in to pause on collision
            #self.paused = True

    def createDebris(self, sprite):
        for _ in range(0, 25):
            position = Vector2d(sprite.position.x, sprite.position.y)
            debris = Debris(position, self.stage)
            self.stage.addSprite(debris)

    def killShip(self):
        self.explodingCount = 0
        self.lives -= 1
        # if (self.livesList):
        #     ship = self.livesList.pop()
        #     self.stage.removeSprite(ship)

        self.stage.removeSprite(self.ship)
        self.stage.removeSprite(self.ship.thrustJet)
        # self.gameState = 'exploding'
        self.ship.explode()

    def levelUp(self):
        self.numRocks += 1
        self.createRocks(self.numRocks)

    def displayScore(self):
        font1 = pygame.font.Font('../../res/Hyperspace.otf', 30)
        scoreStr = str("%02d" % self.score)
        scoreText = font1.render(scoreStr, True, (200, 200, 200))
        scoreTextRect = scoreText.get_rect(centerx=100, centery=45)
        self.stage.screen.blit(scoreText, scoreTextRect)
