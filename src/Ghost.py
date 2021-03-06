# Ghost.py
# authors: Taylor Rongaus & Henry Long

import sys, pygame
from random import randint
import Player as p

# a class for the Ghost computer -- includes initialization of the sprite
# and details on how the movements are generated and updated

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
		self.dir = 0;
		self.speed = 8;
		self.switchcount = 0;
		self.player1 = p.Player(self)
		self.refresh(gs)

	# refresh the movepos
	def refresh(self, gs):
		self.movepos = [0,0]

	# actually make updates to the gamespace
	def update(self, gs):
		_new = self.rect.move(self.movepos)
		x = int(_new.centerx/self.speed)
		y = int(_new.centery/self.speed)
		if gs.board[y][x] == '1':
			self.rect = _new
			pygame.event.pump()

	# function to semi-randomly change the directions of the ghosts
	def changeDir(self, gs, getx, gety):
		self.switchcount += 1
		currpos = (int(self.rect.centerx/self.speed),int(self.rect.centery/self.speed))
		upx = int(self.rect.centerx/self.speed)
		upy = int(self.rect.centery/self.speed)-1
		downx = int(self.rect.centerx/self.speed)
		downy = int(self.rect.centery/self.speed)+1
		leftx = int(self.rect.centerx/self.speed)-1
		lefty = int(self.rect.centery/self.speed)
		rightx = int(self.rect.centerx/self.speed+1)
		righty = int(self.rect.centery/self.speed)
		random = randint(4, 5)
		_new = self.rect.move(self.movepos)
		x = int(_new.centerx/self.speed)
		y = int(_new.centery/self.speed)
		# check old direction
		# if already moving L/R, continue on path until junction
		# then make a new decision
		# also make sure direction is flipped every 75 times or so
		# for preventative maintenance
		if self.switchcount == 75:
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
			# make some educated determinations based on the current direction and
			# the randomly selected new direction of motion
			if self.dir == 0 or self.dir == 1:
				if gs.board[upy][upx] == '1' or gs.board[downy][downx] == '1':
					try:
						if gety > y and gs.board[downy][downx] == '1' and random == 4:
							self.dir = 3
						elif gety < y and gs.board[upy][upx] == '1' and random == 4:
							self.dir = 2
						elif getx > x and gs.board[righty][rightx] == '1' and random == 4:
							self.dir = 1
						elif getx < x and gs.board[lefty][leftx] == '1' and random == 4:
							self.dir = 0
						elif getx < x and gs.board[lefty][leftx] == '1' and random == 5:
							self.dir = 0
						elif getx > x and gs.board[righty][rightx] == '1' and random == 5:
							self.dir = 1
						elif gety < y and gs.board[upy][upx] == '1' and random == 5:
							self.dir = 2
						elif gety > y and gs.board[downy][downx] == '1' and random == 5:
							self.dir = 3
					except:
						pass
			if self.dir == 2 or self.dir == 3:
				if gs.board[lefty][leftx] == '1' or gs.board[righty][rightx] == '1':
					try:
						if gety > y and gs.board[downy][downx] == '1' and random == 4:
							self.dir = 3
						elif gety < y and gs.board[upy][upx] == '1' and random == 4:
							self.dir = 2
						elif getx > x and gs.board[righty][rightx] == '1' and random == 4:
							self.dir = 1
						elif getx < x and gs.board[lefty][leftx] == '1' and random == 4:
							self.dir = 0
						elif getx < x and gs.board[lefty][leftx] == '1' and random == 5:
							self.dir = 0
						elif getx > x and gs.board[righty][rightx] == '1' and random == 5:
							self.dir = 1
						elif gety < y and gs.board[upy][upx] == '1' and random == 5:
							self.dir = 2
						elif gety > y and gs.board[downy][downx] == '1' and random == 5:
							self.dir = 3
					except:
						pass

	# function to control the movements of the ghosts
	def move(self, gs, color, getx, gety):
		img = '../img/ghost-'
		# check to see if we are in "ghost mode" and all images should be blue/white
		if gs.ghost_mode == False:
			img += color
		else:
			if (gs.time_elapsed >= 10 and gs.time_elapsed <= 20) or (gs.time_elapsed >= 30 and gs.time_elapsed <= 40) or (gs.time_elapsed >= 50 and gs.time_elapsed <= 60):
				img += 'white.png'
			else:
				img += 'dark-blue.png'
		# change the direction of the ghosts movement if necessary
		self.changeDir(gs, getx, gety)
		# get the new direction of movement
		direction = self.dirlist[self.dir]
		# update the ghost sprite image depending on new direction
		if direction == 'left':
			if gs.ghost_mode == False:
				img += '-left.png'
			self.image = pygame.transform.scale2x(pygame.image.load(img))
		elif direction == 'right':
			if gs.ghost_mode == False:
				img += '-right.png'
			self.image = pygame.transform.scale2x(pygame.image.load(img))
		elif direction == 'up':
			if gs.ghost_mode == False:
				img += '-up.png'
			self.image = pygame.transform.scale2x(pygame.image.load(img))
		elif direction == 'down':
			if gs.ghost_mode == False:
				img += '-down.png'
			self.image = pygame.transform.scale2x(pygame.image.load(img))
		# handle the case where we can run off the left and right edges of the board
		if int(self.rect.centery/self.speed) == 29 and int(self.rect.centerx/self.speed) == 3:
			self.rect.centerx = 424
			direction = 'left'
		elif int(self.rect.centery/self.speed) == 29 and int(self.rect.centerx/self.speed) == 53:
			self.rect.centerx = 24
			direction = 'right'
		try: 
			# and if the path to the new point exists, update and refresh
			if gs.board[int(self.rect.centery/self.speed)][int(self.rect.centerx/self.speed)] == '1':
				if direction == 'left':
					self.movepos[0] = self.movepos[0] - self.speed/2
				elif direction == 'right':
					self.movepos[0] = self.movepos[0] + self.speed/2
				elif direction == 'up':
					self.movepos[1] = self.movepos[1] - self.speed/2
				elif direction == 'down':
					self.movepos[1] = self.movepos[1] + self.speed/2
				self.update(gs)
				self.refresh(gs)
		except:
			pass
