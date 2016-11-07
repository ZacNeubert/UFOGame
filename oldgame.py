import functions
import pygame 
import math
import sys 

def rotate(vector, angle):
	rotator = [[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]]
	othervector = [ 0,  0 ]
	othervector[0] = vector[0] * rotator[0][0] + vector[0] * rotator[0][1]
	othervector[1] = vector[1] * rotator[1][0] + vector[1] * rotator[1][1]
	return othervector

class projectile(pygame.sprite.Sprite):	
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.speed = [1, 1]
		self.blank = 30
		self.length = 512 - self.blank
		self.pos = [10, 10]
		self.imageMain = pygame.image.load(spriteImg).convert()
		self.image = pygame.image.load(spriteImg).convert()
		self.count = 0
		self.rect = self.image.get_rect()
		self.rect.center = (self.pos[0], self.pos[1])
		self.dir = "clock"
		self.angle = -25

	def update(self):
 		if self.pos[1] > screenY - self.length/2:
			self.speed[1]=-1
		if self.pos[0] > screenX - self.length/2:
			self.speed[0]=-1
		if self.pos[1] < self.length/2:
			self.speed[1]=1
		if self.pos[0] < self.length/2:
			self.speed[0]=1
		self.count+=1
		
		self.pos[0]+=self.speed[0]
		self.pos[1]+=self.speed[1]
		
#		#print self.pos
#		if self.count % 50 == 0:
##			if self.dir is "clock":
#				self.dir = "counterclock"
#			else:
#				self.dir = "clock"

		self.rotate()
#		screen.blit(self.image, (self.pos[0], self.pos[1]))

	def rotate(self):
		self.oldcenter = self.rect.center
		if self.dir is "clock":
			self.angle+=1
		else:
			self.angle-=1
                self.image = pygame.transform.rotate(self.imageMain, self.angle)
#		#print self.dir
                self.rect = self.image.get_rect()
                self.rect.center = self.oldcenter
		self.rect.centerx = round(self.pos[0],0)
		self.rect.centery = round(self.pos[1],1)
		#print self.rect.center
		
pygame.init()

backgroundImg = "back.jpg"
spriteImg = "sprite.png"

screenX = 1600
screenY = 1200
screenX/=3
screenY/=3
screenX*=2
screenY*=2
screen = pygame.display.set_mode((screenX, screenY), 0, 32)
pygame.display.set_caption("Assignment 4")

background_img = pygame.image.load(backgroundImg).convert()

background = pygame.Surface(screen.get_size())
background.fill((0,0,0))

count=0

cat = projectile()
spriteGroup = pygame.sprite.Group(cat)

while True:
	keys = pygame.key.get_pressed()
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			pass
#		        if event.key == pygame.K_LEFT:
#		            cat.rotate(1)
#		        if event.key == pygame.K_RIGHT:
#		            location += 1
		if event.type == pygame.QUIT:
			del background_img
			pygame.display.quit()
			exit(0)
		

	spriteGroup.update()
	screen.blit(background_img, (0,0))
	spriteGroup.draw(screen)
	pygame.display.flip()
