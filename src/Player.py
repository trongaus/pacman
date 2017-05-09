# Player1.py
# authors: Taylor Rongaus & Henry Long

import sys, pygame

class Player(pygame.sprite.Sprite):

	# initialize the pacman player sprite
	def __init__(self, gs):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale2x(pygame.image.load("../img/pacman-left-closed.png"))
		self.rect = self.image.get_rect()
		self.rect.centerx = gs.rect.centerx
		self.rect.centery = gs.rect.centery + 128
		self.speed = 8
		self.refresh(gs)
		self.x = 28
		self.y = 47

	def refresh(self, gs):
		self.movepos = [0,0]

	def getx(self, gs):
		return self.x

	def gety(self, gs):
		return self.y

	def update(self, gs):
		_new = self.rect.move(self.movepos)
		x = int(_new.centerx/self.speed)
		y = int(_new.centery/self.speed)
		self.x = x
		self.y = y
		if gs.board[y][x] == '1':
			gs.travelled[y][x] = '2'
			gs.screen.blit(gs.black_square, (x*self.speed, y*self.speed))
			self.rect = _new
			pygame.event.pump()

	# move the pacman piece and update the image depending on the direction
	def move(self, gs):
		# start by updating the image regardless of if there's a barrier
		if gs.moveDir == 'left':
			self.image = pygame.transform.scale2x(pygame.image.load("../img/pacman-left-closed.png"))
		elif gs.moveDir == 'right':
			self.image = pygame.transform.scale2x(pygame.image.load("../img/pacman-right-closed.png"))
		elif gs.moveDir == 'up':
			self.image = pygame.transform.scale2x(pygame.image.load("../img/pacman-up-closed.png"))
		elif gs.moveDir == 'down':
			self.image = pygame.transform.scale2x(pygame.image.load("../img/pacman-down-closed.png"))
		if int(self.rect.centery/self.speed) == 29 and int(self.rect.centerx/self.speed) == 3:
			self.rect.centerx = 424
			gs.moveDir = 'left'
		elif int(self.rect.centery/self.speed) == 29 and int(self.rect.centerx/self.speed) == 53:
			self.rect.centerx = 24
			gs.moveDir = 'right'
		# then check the board of 0s and 1s - if its a 1, there's a path so you can take it
		try: 
			if gs.board[int(self.rect.centery/self.speed)][int(self.rect.centerx/self.speed)] == '1':
				if gs.moveDir == 'left':
					self.movepos[0] = self.movepos[0] - self.speed
				elif gs.moveDir == 'right':
					self.movepos[0] = self.movepos[0] + self.speed
				elif gs.moveDir == 'up':
					self.movepos[1] = self.movepos[1] - self.speed
				elif gs.moveDir == 'down':
					self.movepos[1] = self.movepos[1] + self.speed
				self.update(gs)
				self.refresh(gs)
		except:
			pass
		
		
		
