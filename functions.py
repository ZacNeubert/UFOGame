#!/usr/bin/python

import numpy as np
import math
import pygame
import random
from pygame.locals import *
from sys import exit
from sound import play


def rotate(matrix, radians):
    rotator = np.matrix('%r %r ; %r %r' % (math.cos(radians), -math.sin(radians), math.sin(radians), math.cos(radians)))
    return rotator * matrix


def update(matrix):
    updator = np.matrix('1 0 0 ; 1 1 0 ; 0 1 1')
    return matrix * updator


def getCol(matrix, c):
    return matrix.transpose()[c]


def pos(state):
    return state.transpose()[0]


def vel(state):
    return state.transpose()[1]


def acc(state):
    return state.transpose()[2]


def leng(matrix, row):
    return len(matrix[row].tolist()[0])


def lengr(matrix, row):
    return len(matrix[row].tolist()[0])


def lengc(matrix, col):
    return leng(matrix.transpose(), col)


def dist(pos1, pos2):
    return math.sqrt((pos2.X() - pos1.X()) ** 2 + (pos2.Y() - pos1.Y()) ** 2)


def dist(pos1, X, Y):
    return math.sqrt((X - pos1.X()) ** 2 + (Y - pos1.Y()) ** 2)


def getAngle(pos1, pos2):
    deltaX = pos2.X() - pos1.X()
    deltaY = pos2.Y() - pos1.Y()
    angle = math.atan2(deltaY, deltaX)
    return angle


def getAngle(pos1, X, Y):
    deltaX = X - pos1.X()
    deltaY = Y - pos1.Y()
    angle = math.atan2(deltaY, deltaX)
    return angle


def getUnitVector(angle):
    return np.matrix([[math.cos(angle)],
                      [math.sin(angle)]])


def getRadians(deg):
    return (deg / 180.0) * math.pi


class Projectile(pygame.sprite.Sprite):
    def __init__(self, spriteImgList, screen, X, Y, screenX, screenY):
        pygame.sprite.Sprite.__init__(self)
        self.screenX = screenX
        self.screenY = screenY
        self.length = 30
        self.state = np.matrix([[float(X), 0.0, 0.0],
                                [float(Y), 0.0, 0.0]])
        self.dead = False
        self.imageMainList = [pygame.image.load(im).convert() for im in spriteImgList]
        self.imageList = [pygame.image.load(im).convert() for im in spriteImgList]
        self.imageIndex = 0
        self.deadImage = self.imageMainList[-1]
        self.imageMain = self.imageMainList[self.imageIndex]
        self.image = self.imageList[self.imageIndex]
        self.count = 0
        self.rect = self.image.get_rect()
        self.rect.center = (self.X(), self.Y())
        self.angle = 0
        self.debounce = 0
        self.maxSpeed = 5.0
        self.wallDebounce = 0
        self.colldebounce = 0
        self.skipImageChange = 0
        self.shielded = 45
        self.shields = 3

    def getShieldSprites(self, shieldedSprites):
        self.shieldedSprites = [pygame.image.load(im).convert() for im in shieldedSprites]

    def kill(self):
        if not self.isShielded():
            self.image = self.deadImage
            self.imageMain = self.deadImage
            self.dead = True

    def isShielded(self):
        return self.shielded > 0

    def update(self):
        if self.dead:
            return
        if self.wallDebounce == 0:
            self.wallBounced = False
        if self.Y() > self.screenY - self.length:
            self.reverseY()
            self.setY(self.screenY - self.length)
            self.wallBounced = True
        if self.X() > self.screenX - self.length:
            self.wallBounced = True
            self.reverseX()
            self.setX(self.screenX - self.length)
        if self.Y() < 0:
            self.wallBounced = True
            self.reverseY()
            self.setY(0)
        if self.X() < 0:
            self.wallBounced = True
            #            print "4"
            self.setX(0)
            self.reverseX()
        if self.wallBounced:
            self.wallDebounce = 15
        self.count += 1
        if self.debounce > 0:
            self.debounce -= 1
        if self.wallDebounce > 0:
            self.wallDebounce -= 1
        if self.colldebounce > 0:
            self.colldebounce -= 1

        self.state = update(self.state)
        if self.speed() > self.maxSpeed:
            x = self.state[0, 1]
            y = self.state[1, 1]
            ratio = self.speed() / self.maxSpeed
            x = x / ratio
            y = y / ratio
            self.state[0, 1] = x
            self.state[1, 1] = y
        self.resetAcc()
        if len(self.imageList) - 1 != 0:
            if not self.skipImageChange:
                self.imageIndex = (self.imageIndex + 1) % (len(self.imageList) - 1)
                if not self.isShielded():
                    self.image = self.imageList[self.imageIndex]
                    self.imageMain = self.imageMainList[self.imageIndex]
                else:
                    self.image = self.shieldedSprites[self.imageIndex]
                    self.imageMain = self.image
                    self.shielded -= 1
            self.skipImageChange = (self.skipImageChange + 1) % 3  # 20

        self.rect = pygame.Rect(self.X(), self.Y(), self.length, self.length)

    def resetAcc(self):
        self.state[0, 2] = 0.0
        self.state[1, 2] = 0.0

    def startShield(self):
        if self.shields > 0:
            self.shielded = 45
            self.shields -= 1
            return play("shield.wav", 1.6)
        self.shields -= 1
        return play("silence.wav", .1)

    def speed(self):
        return math.sqrt(self.state[0, 1] ** 2 + self.state[1, 1] ** 2)

    def reverse(self):
        self.state = self.state * np.matrix('1 0 0 ; 0 -1 0 ; 0 0 1')

    def reverseX(self):
        self.state[0, 1] = -self.state[0, 1]

    def reverseY(self):
        self.state[1, 1] = -self.state[1, 1]

    def X(self):
        return self.state[0, 0]

    def Y(self):
        return self.state[1, 0]

    def setX(self, x):
        self.state[0, 0] = x

    def setY(self, y):
        self.state[1, 0] = y

    def pos(self):
        return getCol(self.state(), 0)

    def getAccX(self):
        return self.state[0, 2]

    def getAccY(self):
        return self.state[1, 2]

    def setAccX(self, accx):
        self.state[0, 2] = accx

    def setAccY(self, accy):
        self.state[1, 2] = accy

    def getVelX(self):
        return self.state[0, 1]

    def getVelY(self):
        return self.state[1, 1]

    def setVelX(self, velx):
        self.state[0, 1] = velx

    def setVelY(self, vely):
        self.state[1, 1] = vely

    def rotate(self, angle):
        self.oldcenter = self.rect.center
        self.angle += angle
        self.image = pygame.transform.rotate(self.imageMain, self.angle)
        self.speed.rotate(angle)
        self.acc.rotate(angle)
        #        print self.dir
        self.rect = self.image.get_rect()
        self.rect.center = self.oldcenter
        self.rect.centerx = round(self.X(), 0)
        self.rect.centery = round(self.Y(), 1)


class Asteroid(Projectile):
    def __init__(self, spriteImg, screen, X, Y, screenX, screenY, which):
        Projectile.__init__(self, spriteImg, screen, X, Y, screenX, screenY)
        self.colldebounce = 0
        self.shielded = -1
        self.state[0, 1] = float(random.randint(-200, 200)) / 100.0
        self.state[1, 1] = float(random.randint(-200, 200)) / 100.0
