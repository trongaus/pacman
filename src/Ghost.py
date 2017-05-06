# Ghost.py
# authors: Taylor Rongaus & Henry Long

import sys, pygame
from random import randint
import Player1 as p1

class Ghost(pygame.sprite.Sprite):

	# initialize the ghost sprite
	def __init__(self, gs, png):
		pygame.sprite.Sprite.__init__(self)
		imgpath = "../img/"
		imgpath += png
		self.image = pygame.image.load(imgpath)
		self.image = pygame.transform.scale2x(self.image)
		self.rect = self.image.get_rect()
		self.rect.centerx = gs.rect.centerx
		self.rect.centery = gs.rect.centery - 20
		self.dirlist = ['left', 'right', 'up', 'down']
		self.dir = ;
		self.speed = 8;
		self.switchcount = 0;
		self.player1 = p1.Player1(self)
		self.refresh(gs)

	def refresh(self, gs):
		self.movepos = [0,0]

	def update(self, gs):
		_new = self.rect.move(self.movepos)
		x = int(_new.centerx/self.speed)
		y = int(_new.centery/self.speed)
		if gs.board[y][x] == '1':
			self.rect = _new
			pygame.event.pump()

	# function to semi-randomly change the directions of the ghosts
	def changeDir(self, gs):
		#self.switchcount += 1
		#olddir = self.dir
		currpos = (int(self.rect.centerx/self.speed),int(self.rect.centery/self.speed))
		upx = int(self.rect.centerx/self.speed)
		upy = int(self.rect.centery/self.speed)-1
		downx = int(self.rect.centerx/self.speed)
		downy = int(self.rect.centery/self.speed)+1
		leftx = int(self.rect.centerx/self.speed)-1
		lefty = int(self.rect.centery/self.speed)
		rightx = int(self.rect.centerx/self.speed+1)
		righty = int(self.rect.centery/self.speed)
		# check old direction
		# if already moving L/R, continue on path until junction
		# then make a new decision
		if self.switchcount == 100:
			if self.dir == 0:
				self.dir = 1
			elif self.dir == 1:
				self.dir = 0
			elif self.dir == 2:
				self.dir = 3
			elif self.dir == 3:
				self.dir = 2
			self.switchcount = 0
		else:
			if self.dir == 0 or self.dir == 1:
				if gs.board[upy][upx] == '1' or gs.board[downy][downx] == '1':
					#if self.player1.movepos[1] > movepos
					self.dir = randint(0,3)
			if self.dir == 2 or self.dir == 3:
				if gs.board[lefty][leftx] == '1' or gs.board[righty][rightx] == '1':
					self.dir = randint(0,3)
		'''_new = self.rect.move(self.movepos)
		x = int(_new.centerx/self.speed)
		y = int(_new.centery/self.speed)
		if self.dir == 1 and gs.board[y]'''


	def move(self, gs, color):
		# start by updating the image regardless of if there's a barrier
		img = '../img/ghost-'
		img += color
		self.changeDir(gs)
		direction = self.dirlist[self.dir]
		if direction == 'left':
			img += '-left.png'
			self.image = pygame.transform.scale2x(pygame.image.load(img))
		elif direction == 'right':
			img += '-right.png'
			self.image = pygame.transform.scale2x(pygame.image.load(img))
		elif direction == 'up':
			img += '-up.png'
			self.image = pygame.transform.scale2x(pygame.image.load(img))
		elif direction == 'down':
			img += '-down.png'
			self.image = pygame.transform.scale2x(pygame.image.load(img))
		try: 
			if gs.board[int(self.rect.centery/self.speed)][int(self.rect.centerx/self.speed)] == '1':
				if direction == 'left':
					self.movepos[0] = self.movepos[0] - self.speed/4
				elif direction == 'right':
					self.movepos[0] = self.movepos[0] + self.speed/4
				elif direction == 'up':
					self.movepos[1] = self.movepos[1] - self.speed/4
				elif direction == 'down':
					self.movepos[1] = self.movepos[1] + self.speed/4
				self.update(gs)
				self.refresh(gs)
		except:
			pass
