# Ghost.py
# authors: Taylor Rongaus & Henry Long

import sys, pygame

class Ghost(pygame.sprite.Sprite):
	def __init__(self, gs, png):
		pygame.sprite.Sprite.__init__(self)
		imgpath = "../img/"
		imgpath += png
		self.image = pygame.image.load(imgpath)
		self.image = pygame.transform.scale2x(self.image)
		self.rect = self.image.get_rect()
		self.rect.centerx = gs.rect.centerx
		self.rect.centery = gs.rect.centery - 20