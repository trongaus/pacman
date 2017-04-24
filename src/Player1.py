# Player1.py
# authors: Taylor Rongaus & Henry Long

import sys, pygame

class Player1(pygame.sprite.Sprite):

	# initialize the pacman player sprite
	def __init__(self, gs):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale2x(pygame.image.load("../img/pacman-left-closed.png"))
		self.rect = self.image.get_rect()
		self.rect.centerx = gs.rect.centerx
		self.rect.centery = gs.rect.centery + 128
		self.speed = 8
		self.refresh()

	def refresh(self):
		self.movepos = [0,0]

	def update(self):
		_new = self.rect.move(self.movepos)
		self.rect = _new
		pygame.event.pump()

	# move the pacman piece and update the image depending on the direction
	def move(self, direction):
		if direction == 'left':
			self.movepos[0] = self.movepos[0] - self.speed
			self.image = pygame.transform.scale2x(pygame.image.load("../img/pacman-left-closed.png"))
			self.update()
		elif direction == 'right':
			self.movepos[0] = self.movepos[0] + self.speed
			self.image = pygame.transform.scale2x(pygame.image.load("../img/pacman-right-closed.png"))
			self.update()
		elif direction == 'up':
			self.movepos[1] = self.movepos[1] - self.speed
			self.image = pygame.transform.scale2x(pygame.image.load("../img/pacman-up-closed.png"))
			self.update()
		elif direction == 'down':
			self.movepos[1] = self.movepos[1] + self.speed
			self.image = pygame.transform.scale2x(pygame.image.load("../img/pacman-down-closed.png"))
			self.update()
		self.refresh()
		
		
		
