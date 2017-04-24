# Player1.py
# authors: Taylor Rongaus & Henry Long

import sys, pygame

class Player1(pygame.sprite.Sprite):
	def __init__(self, gs):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("../img/pacman-left-closed.png")
		self.image = pygame.transform.scale2x(self.image)
		self.rect = self.image.get_rect()
		self.rect.centerx = gs.rect.centerx
		self.rect.centery = gs.rect.centery + 128