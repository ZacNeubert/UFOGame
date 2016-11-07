import pygame
import math
from pygame.locals import *
from sys import exit

def getAngle(pos1, pos2):
	pass

def getRadians(deg):
	return (deg/180.0)*math.pi

class projectile(pygame.sprite.Sprite):	
	def __init__(self, spriteImg, screen, X, Y, screenX, screenY):
		pygame.sprite.Sprite.__init__(self)
		self.screenX = screenX
		self.screenY = screenY
		self.speed = [1, 1]
		self.length = 30
		
		self.imageMain = pygame.image.load(spriteImg).convert()
		self.image = pygame.image.load(spriteImg).convert()
		self.count = 0
		self.rect = self.image.get_rect()
		self.rect.center = (self.pos.x(), self.pos.y())
		self.angle = -25
		self.friction = matrix([[.95, 0], [0, .95]])

	def update(self):
 		if self.pos.y() > self.screenY - self.length/2:
			self.speed.multY(-1)
		if self.pos.x() > self.screenX - self.length/2:
			self.speed.multX(-1)
		if self.pos.y() < self.length/2:
			self.speed.multY(-1)
		if self.pos.x() < self.length/2:
			self.speed.multX(-1)
		self.count+=1
		
#		self.speed = self.speed.vectormult(self.friction)
		self.pos.addX(self.speed.x())
		self.pos.addY(self.speed.y())
		self.rect = pygame.Rect(self.pos.x(), self.pos.y(), self.length, self.length)
		
##		self.speed.addX(self.acc.x())
#		self.speed.addY(self.acc.y())
#		#print self.pos
#		self.rotate()
#		self.screen.blit(self.image, (self.pos.x(), self.pos.y()))

	def rotate(self, angle):
		self.oldcenter = self.rect.center
		self.angle+=angle
                self.image = pygame.transform.rotate(self.imageMain, self.angle)
		self.speed.rotate(angle)
		self.acc.rotate(angle)
#		#print self.dir
                self.rect = self.image.get_rect()
                self.rect.center = self.oldcenter
		self.rect.centerx = round(self.pos.x(),0)
		self.rect.centery = round(self.pos.y(),1)
		#print self.rect.center


class angryThing(projectile):
	def __init__(self, spriteImg, screen, X, Y, screenX, screenY, which):
		projectile.__init__(self, spriteImg, screen, X, Y, screenX, screenY)
		self.speed.setX(.25)

	def reverse(self):
		self.speed.multX(-1)
		self.speed.multY(-1)
