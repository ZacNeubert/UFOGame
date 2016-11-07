#!/usr/bin/python

import numpy as np
import math
import pygame
import random
from pygame.locals import *
from functions import *
from sys import exit
from sound import play


class hazard(pygame.sprite.Sprite):
    def __init__(self, spriteImgList, X, Y, lengthY, lengthX):
        pygame.sprite.Sprite.__init__(self)
        self.lengthX = lengthX
        self.lengthY = lengthY
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
        self.imageChangeFreq = 5
        self.specImages = 2

    def kill(self):
        self.image = self.deadImage
        self.imageMain = self.deadImage
        self.dead = True

    def update(self):
        if self.dead:
            return
        if not self.skipImageChange:
            self.imageIndex = (self.imageIndex + 1) % (len(self.imageList) - self.specImages)
            self.image = self.imageList[self.imageIndex]
            self.imageMain = self.imageMainList[self.imageIndex]
        self.skipImageChange = (self.skipImageChange + 1) % self.imageChangeFreq
        self.rect = pygame.Rect(self.X(), self.Y(), self.lengthX, self.lengthY)

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


class lazer(hazard):
    def __init__(self, X, soundFile, life=999999, chtime=50, adjs=0):
        hazard.__init__(self, ["Hazards/lazers/lazerbstack.png", "Hazards/lazers/lazerrstack.png",
                               "Hazards/lazers/chargingstack.png", "Hazards/lazers/lazerred.png"], X, -10, 640, 50)
        self.soundf = soundFile
        self.chsoundf = random.choice(["lazers/focus.wav", "lazers/focus+1.wav", "lazers/focus-2.wav"])
        self.image = self.imageList[-2]
        self.imageMain = self.imageMainList[-2]
        self.age = 0
        self.life = life
        self.charging = True
        self.chtime = chtime
        self.playedbzz = False
        self.adjs = adjs

    def update(self):
        hazard.update(self)
        self.age += 1
        self.charging = self.age < self.chtime
        if self.charging:
            self.skipImageChange = 1
            self.image = self.imageList[-2]
            self.imageMain = self.imageMainList[-2]
        if self.age > self.life:
            self.kill()

    def kill(self):
        hazard.kill(self)
        self.lengthX = 1
        self.lengthY = 1
        self.setX(-100)
        self.rect = pygame.Rect(self.X(), self.Y(), self.lengthX, self.lengthY)

    def playSound(self):
        self.playedbzz = True
        self.setX(self.X() - 10)
        self.rect = pygame.Rect(self.X(), self.Y(), self.lengthX, self.lengthY)
        return play(self.soundf, .5)

    def playChSound(self):
        return play(self.chsoundf, .9)

    def getAdjLazer(self, sf):
        if sf == "":
            sf = self.soundf
        print("Getting adjacent laser V")
        self.newX = self.X()
        self.mod = 60
        if random.randint(0, 5) % 2 == 0:
            self.newX += self.mod
        else:
            self.newX -= self.mod
        return lazer(self.newX, sf, self.life, self.chtime, self.adjs + 1)


class hlazer(hazard):
    def __init__(self, Y, soundFile, life=999999, chtime=50, adjs=0):
        hazard.__init__(self, ["Hazards/lazers/rlazerbstack.png", "Hazards/lazers/rlazerrstack.png",
                               "Hazards/lazers/rchargingstack.png", "Hazards/lazers/rlazerred.png"], -10, Y, 50, 640)
        self.soundf = soundFile
        self.chsoundf = "lazers/focus.wav"
        self.image = self.imageList[-2]
        self.imageMain = self.imageMainList[-2]
        self.age = 0
        self.life = life
        self.charging = True
        self.chtime = chtime
        self.playedbzz = False
        self.adjs = adjs

    def update(self):
        hazard.update(self)
        self.age += 1
        self.charging = self.age < self.chtime
        if self.charging:
            self.skipImageChange = 1
            self.image = self.imageList[-2]
            self.imageMain = self.imageMainList[-2]
        if self.age > self.life:
            self.kill()

    def kill(self):
        hazard.kill(self)
        self.lengthX = 1
        self.lengthY = 1
        self.rect = pygame.Rect(self.X(), self.Y(), self.lengthX, self.lengthY)
        self.setY(-100)

    def playSound(self):
        self.playedbzz = True
        self.setY(self.Y() - 10)
        self.rect = pygame.Rect(self.X(), self.Y(), self.lengthX, self.lengthY)
        return play(self.soundf, .5)

    def playChSound(self):
        return play(self.chsoundf, .7)

    def getAdjLazer(self, sf):
        if sf == "":
            sf = self.soundf
        print("Getting adjacent laser H")
        self.newY = self.Y()
        self.mod = 60
        if random.randint(0, 5) % 2 == 0:
            self.newY += self.mod
        else:
            self.newY -= self.mod
        return hlazer(self.newY, sf, self.life, self.chtime, self.adjs + 1)


class wormhole():
    def __init__(self, black, white):
        self.black = black
        self.white = white

    def teleport(self, hole, tars):
        tars.setX(self.white.centerX())
        tars.setY(self.white.centerY())
        return play(random.choice(["bloop.wav", "bloop-2.wav", "bloop-5.wav"]))


class blackhole(hazard):
    def __init__(self, spriteImgList, X, Y, lengthY, lengthX, gravity):
        hazard.__init__(self, spriteImgList, X, Y, lengthY, lengthX)
        self.gravity = gravity
        self.imageChangeFreq = 5
        self.specImages = 0

    def alterAcc(self, tars):
        angle = getAngle(tars, self.centerX(), self.centerY())
        accVec = getUnitVector(angle)
        accVec = accVec * self.gravity
        tars.setAccX(tars.getAccX() + accVec[0, 0])
        tars.setAccY(tars.getAccY() + accVec[1, 0])

    def centerX(self):
        return self.X() + (self.lengthX / 2)

    def centerY(self):
        return self.Y() + (self.lengthY / 2)


class menu():
    def __init__(self, buttonList):
        self.buttonList = buttonList
        self.bindex = 0
        self.buttonList[self.bindex].selected = True

    def change(self):
        self.buttonList[self.bindex].selected = False
        self.bindex += 1
        if self.bindex == len(self.buttonList):
            self.bindex = 0
        self.buttonList[self.bindex].selected = True

    def revChange(self):
        self.buttonList[self.bindex].selected = False
        self.bindex -= 1
        if self.bindex < 0:
            self.bindex = len(self.buttonList) - 1
        self.buttonList[self.bindex].selected = True


class button(hazard):
    def __init__(self, imageList, X, Y):
        hazard.__init__(self, imageList, X, Y, 180, 90)
        self.specImages = 1
        self.selected = False

    def update(self):
        hazard.update(self)
        if self.selected:
            self.image = self.imageList[-1]
            self.imageMain = self.imageList[-1]
        else:
            self.image = self.imageList[0]
            self.imageMain = self.imageList[0]
