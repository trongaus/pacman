# main.py
# authors: Taylor Rongaus & Henry Long

import sys, pygame
import Player1 as p1
import Ghost as gh
from twisted.internet.task import LoopingCall

class GameSpace:

	# main gamsepace and sprites initialization
	def __init__(self):
		pygame.init()
		self.clock = pygame.time.Clock()
		self.sound = "../sounds/pacman_waka.wav"
		self.size = self.width, self.height = 640, 496
		self.black = 0,0,0
		self.black_square = pygame.transform.scale2x(pygame.image.load("../img/black-square.png"))
		self.screen = pygame.display.set_mode(self.size)
		self.board = [[]]
		self.readBoard()
		self.travelled = [[]]
		self.readTravelled()
		self.lives = 3
		self.ghost_mode = False
		self.time_elapsed = 240
		self.release_time = 719
		self.largeDots = [False, False, False, False]
		pygame.display.set_caption('Pac-Man')
		self.font = pygame.font.SysFont("liberationsans", 15)
		self.logo = pygame.image.load("../img/logo.png")
		self.logorect = self.logo.get_rect()
		self.logorect.centerx = 546
		self.logorect.centery = 28
		self.image = pygame.image.load("../img/full-board.png")
		self.image = pygame.transform.scale2x(self.image)
		self.rect = self.image.get_rect()
		self.rect.centerx = 224 
		self.rect.centery = 248
		self.player1 = p1.Player1(self)
		self.red_ghost = gh.Ghost(self,"ghost-red-up.png")
		self.red_ghost.rect.centerx -= 60
		self.red_ghost.rect.centery -= 42
		self.blue_ghost = gh.Ghost(self, "ghost-blue-up.png")
		self.blue_ghost.rect.centerx -= 20
		self.blue_ghost.rect.centery -= 42
		self.pink_ghost = gh.Ghost(self, "ghost-pink-up.png")
		self.pink_ghost.rect.centerx += 20
		self.pink_ghost.rect.centery -= 42
		self.orange_ghost = gh.Ghost(self, "ghost-orange-up.png")
		self.orange_ghost.rect.centerx += 60
		self.orange_ghost.rect.centery -= 42

	# read in the board.txt file as a 2D array
	def readBoard(self):
		with open('board.txt') as file:
			self.board = [[digit for digit in line.split()] for line in file]

	# read in the dots.txt file as a 2D array
	def readTravelled(self):
		with open('dots.txt') as file:
			self.travelled = [[digit for digit in line.split()] for line in file]

	# blit all changes to the screen
	def update(self):
		self.screen.fill(self.black)
		self.screen.blit(self.image, self.rect)
		self.screen.blit(self.logo, self.logorect)
		self.coverDots()
		self.screen.blit(self.player1.image, self.player1.rect)
		self.screen.blit(self.red_ghost.image, self.red_ghost.rect)
		self.screen.blit(self.blue_ghost.image, self.blue_ghost.rect)
		self.screen.blit(self.pink_ghost.image, self.pink_ghost.rect)
		self.screen.blit(self.orange_ghost.image, self.orange_ghost.rect)

	# cover the necessary dots
	def coverDots(self):
		i=0
		j=0
		for row in self.travelled:
			i = i + 1
			for col in row:
				j = j + 1
				if col == '2':
					self.screen.blit(self.black_square, (j*self.player1.speed-(2*(self.player1.speed)),i*self.player1.speed-(2*(self.player1.speed))))
			j = 0

	# function specific to updates made during gameplay
	def ingameUpdate(self):
		self.update()
		# blit black over the dots we have covered
		text = "LIVES: "
		text += str(self.lives)
		self.screen.blit(self.font.render(text, 1, (255,255,255)), (456, 72))
		pygame.display.update()	

	# run this function until one of the start buttons are pressed
	def start(self):
		try:
			pygame.mixer.music.load("../sounds/pacman_beginning.wav")
			pygame.mixer.music.play()
		except:
			print("Error loading ../sounds/pacman_beginning.wav")
		self.update()
		# update the screen with the directions and start button
		pygame.draw.rect(self.screen, (255,255,255), (494,140,100,30))
		pygame.draw.rect(self.screen, (255,255,255), (494,180,100,30))
		text1 = "Use the arrow keys to move,"
		text2 = "eat all the dots and"
		text3 = "avoid the ghosts."
		text4 = "1 PLAYER"
		text5 = "2 PLAYER"
		directions = self.font.render("DIRECTIONS:", 1, (255,255,255))
		directions1 = self.font.render(text1, 1, (255,255,255))
		directions2 = self.font.render(text2, 1, (255,255,255))
		directions3 = self.font.render(text3, 1, (255,255,255))
		button1 = self.font.render(text4, 1, (0,0,0))
		button2 = self.font.render(text5, 1, (0,0,0))
		self.screen.blit(directions, (500, 56))
		self.screen.blit(directions1, (452, 72))
		self.screen.blit(directions2, (452, 88))
		self.screen.blit(directions3, (452, 104))
		self.screen.blit(button1, (520, 144))
		self.screen.blit(button2, (520, 184))
		pygame.display.update()
		clicked = False
		main1 = False
		main2 = False				
		while not clicked:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					pos = pygame.mouse.get_pos()
					# determine if user clicked w/in the range of the 1P start button
					if pos[0] >= 494 and pos[0] <= 594:
						if pos[1] >= 140 and pos[1] <= 170:
							clicked = True
							main1 = True
					# determine if user clicked w/in the range of the 2P start button
						if pos[1] >= 180 and pos[1] <= 210:
							clicked = True
							main2 = True
		if main1 == True:
			self.main1()
		elif main2 == True:
			self.main2()
		else:
			pass

	# function to check to see if we've run over a large dot
	def checkLargeDot(self):
		x = self.player1.rect.centerx
		y = self.player1.rect.centery
		# check to see if we have run over a dot that hasn't yet been run over
		if (x, y) == (24, 376) and self.largeDots[0] == False:
			self.ghost_mode = True
			self.largeDots[0] = True
			self.time_elapsed = 240
		if (x, y) == (424, 376) and self.largeDots[1] == False: 
			self.ghost_mode = True
			self.largeDots[1] = True
			self.time_elapsed = 240
		if (x, y) == (24, 48) and self.largeDots[2] == False: 
			self.ghost_mode = True
			self.largeDots[2] = True
			self.time_elapsed = 240
		if (x, y) == (424, 48) and self.largeDots[3] == False:
			self.ghost_mode = True
			self.largeDots[3] = True 
			self.time_elapsed = 240
		# check to see if the time has elapsed for ghost mode
		if self.time_elapsed <= 0:
			self.ghost_mode = False
			self.time_elapsed = 240
		else:
			self.time_elapsed = self.time_elapsed - 1

	# function to iterate through the travelled board and determine if the player has won
	def checkWin(self):
		i=0
		j=0
		x = True
		for row in self.travelled:
			i = i + 1
			for col in row:
				j = j + 1
				if col == '1':
					x = False
			j = 0
		return x

	# function to reset the board after a life is lost
	def reset(self):
		try:
			pygame.mixer.music.load("../sounds/pacman_death.wav")
			pygame.mixer.music.play()
		except:
			print("Error loading ../sounds/pacman_death.wav")
		if self.lives > 0:
			pygame.time.wait(1000)
			self.ghost_mode = False
			self.red_ghost = gh.Ghost(self,"ghost-red-up.png")
			self.red_ghost.rect.centerx -= 60
			self.red_ghost.rect.centery -= 42
			self.blue_ghost = gh.Ghost(self, "ghost-blue-up.png")
			self.blue_ghost.rect.centerx -= 20
			self.blue_ghost.rect.centery -= 42
			self.pink_ghost = gh.Ghost(self, "ghost-pink-up.png")
			self.pink_ghost.rect.centerx += 20
			self.pink_ghost.rect.centery -= 42
			self.orange_ghost = gh.Ghost(self, "ghost-orange-up.png")
			self.orange_ghost.rect.centerx += 60
			self.orange_ghost.rect.centery -= 42
			self.player1.rect.centerx = self.rect.centerx
			self.player1.rect.centery = self.rect.centery + 128
			pygame.time.wait(1000)
		else:
			self.gameover("YOU LOSE!")
		try:
			pygame.mixer.music.load(self.sound)
			pygame.mixer.music.play(-1)
		except:
			print("Error loading ../sounds/pacman_waka.wav")

	# function to end the game cleanly upon a loss
	def gameover(self, outcome):
		if outcome == "YOU WON!":
			try:
				pygame.mixer.music.load("../sounds/ta-da.wav")
				pygame.mixer.music.play()
			except:
				print("Error loading ../sounds/ta-da.wav")
		self.screen.fill(self.black)
		pygame.draw.rect(self.screen, (255,255,255), (self.width/2-40, self.height/2,100,30))
		pygame.draw.rect(self.screen, (255,255,255), (self.width/2-40, self.height/2+50,100,30))
		text = outcome
		text2 = " Play again?"
		text3 = "1 PLAYER"
		text4 = "2 PLAYER"
		self.screen.blit(self.font.render(text, 1, (255,255,255)), (self.width/2-20, self.height/2-60))
		self.screen.blit(self.font.render(text2, 1, (255,255,255)), (self.width/2-20, self.height/2-30))
		self.screen.blit(self.font.render(text3, 1, (0,0,0)), (self.width/2-15, self.height/2+10))
		self.screen.blit(self.font.render(text4, 1, (0,0,0)), (self.width/2-15, self.height/2+60))
		pygame.display.update()	
		clicked = False
		main1 = False
		main2 = False
		while not clicked:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					pos = pygame.mouse.get_pos()
					# determine if user clicked w/in the range of either of the start buttons
					if pos[0] >= self.width/2-40 and pos[0] <= self.width/2+60:
						if pos[1] >= self.height/2 and pos[1] <= self.height/2+30:
							clicked = True
							main1 = True
						if pos[1] >= self.height/2+50 and pos[1] <= self.height/2+80:
							clicked = True
							main2 = True
		self.__init__()
		if main1 == True:
			self.main1()
		elif main2 == True:
			self.main2()
		else: 
			pass

	# main1 begins once we press the player 1 start button
	def main1(self):
		pygame.key.set_repeat(1,100)
		# need to figure out how to add in the proper sound effects
		try:
			pygame.mixer.music.load(self.sound)
			pygame.mixer.music.play(-1)
		except:
			print("Error loading ../sounds/pacman_waka.wav")
		moveDir = ''
		queue = 0
		while 1:
			# clock tick
			self.clock.tick(60)
			# move the ghosts
			self.red_ghost.move(self, 'red', self.player1.getx(gs), self.player1.gety(gs))
			self.blue_ghost.move(self, 'blue', self.player1.getx(gs), self.player1.gety(gs))
			self.pink_ghost.move(self, 'pink', self.player1.getx(gs), self.player1.gety(gs))
			self.orange_ghost.move(self, 'orange', self.player1.getx(gs), self.player1.gety(gs))
			# prepare to check travelled
			_new = self.player1.rect.move(self.player1.movepos)
			x = int(_new.centerx/self.player1.speed)
			y = int(_new.centery/self.player1.speed)
			# see if any new events have occurred
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LEFT:
						if self.board[y][x - 1] == '1':
							moveDir = 'left'
							queue = 1
						else:
							queue = 1
					elif event.key == pygame.K_RIGHT:
						if self.board[y][x + 1] == '1':
							moveDir = 'right'
							queue = 2
						else:
							queue = 2
					elif event.key == pygame.K_UP:
						if self.board[y - 1][x] == '1':
							moveDir = 'up'
							queue = 3
						else:
							queue = 3
					elif event.key == pygame.K_DOWN:
						if self.board[y + 1][x] == '1':
							moveDir = 'down'
							queue = 4
						else:
							queue = 4
			if queue == 1 and self.board[y][x - 1] == '1':
				moveDir = 'left'
			elif queue == 2 and self.board[y][x + 1] == '1':
				moveDir = 'right'
			elif queue == 3 and self.board[y - 1][x] == '1':
				moveDir = 'up'
			elif queue == 4 and self.board[y + 1][x] == '1':
				moveDir = 'down'
			# move the pac and update the changes to the screen
			self.player1.move(self, moveDir)
			self.ingameUpdate()
			# check to see if we've run over a large dot
			self.checkLargeDot()
			# check to see if we have collided with a ghost
			if self.ghost_mode == False:
				if (self.player1.rect.colliderect(self.red_ghost.rect) or self.player1.rect.colliderect(self.blue_ghost.rect)) or self.player1.rect.colliderect(self.pink_ghost.rect) or self.player1.rect.colliderect(self.orange_ghost.rect):
					self.lives -= 1
					self.reset()
			# check to see if we have won
			if self.checkWin() == True:
				self.gameover("YOU WON!")
			# update the screen
			pygame.display.flip()

	# function to hold the stuff in the while loop
	def loopFunction(self):
		# clock tick
		# self.clock.tick(60)
		# move the ghosts
		print("entered loop function")
		self.red_ghost.move(self, 'red', self.player1.getx(gs), self.player1.gety(gs))
		self.blue_ghost.move(self, 'blue', self.player1.getx(gs), self.player1.gety(gs))
		self.pink_ghost.move(self, 'pink', self.player1.getx(gs), self.player1.gety(gs))
		self.orange_ghost.move(self, 'orange', self.player1.getx(gs), self.player1.gety(gs))
		# prepare to check travelled
		_new = self.player1.rect.move(self.player1.movepos)
		x = int(_new.centerx/self.player1.speed)
		y = int(_new.centery/self.player1.speed)
		# see if any new events have occurred
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					if self.board[y][x - 1] == '1':
						moveDir = 'left'
						queue = 1
					else:
						queue = 1
				elif event.key == pygame.K_RIGHT:
					if self.board[y][x + 1] == '1':
						moveDir = 'right'
						queue = 2
					else:
						queue = 2
				elif event.key == pygame.K_UP:
					if self.board[y - 1][x] == '1':
						moveDir = 'up'
						queue = 3
					else:
						queue = 3
				elif event.key == pygame.K_DOWN:
					if self.board[y + 1][x] == '1':
						moveDir = 'down'
						queue = 4
					else:
						queue = 4
		if queue == 1 and self.board[y][x - 1] == '1':
			moveDir = 'left'
		elif queue == 2 and self.board[y][x + 1] == '1':
			moveDir = 'right'
		elif queue == 3 and self.board[y - 1][x] == '1':
			moveDir = 'up'
		elif queue == 4 and self.board[y + 1][x] == '1':
			moveDir = 'down'
		# move the pac and update the changes to the screen
		self.player1.move(self, moveDir)
		self.ingameUpdate()
		# check to see if we've run over a large dot
		self.checkLargeDot()
		# check to see if we have collided with a ghost
		if self.ghost_mode == False:
			if (self.player1.rect.colliderect(self.red_ghost.rect) or self.player1.rect.colliderect(self.blue_ghost.rect)) or self.player1.rect.colliderect(self.pink_ghost.rect) or self.player1.rect.colliderect(self.orange_ghost.rect):
				self.lives -= 1
				self.reset()
		# check to see if we have won
		if self.checkWin() == True:
			self.gameover("YOU WON!")
		# update the screen
		pygame.display.flip()

	# main begins once we press the start button
	def main2(self):
		print("main 2")
		pygame.key.set_repeat(1,100)
		# need to figure out how to add in the proper sound effects
		try:
			pygame.mixer.music.load(self.sound)
			pygame.mixer.music.play(-1)
		except:
			print("Error loading ../sounds/pacman_waka.wav")
		moveDir = ''
		queue = 0
		# use LoopingCall(1/60) instead of while
		# designate someone as the "master copy" -- hopefully it's close enough
		# every second or so, send the client the current position  
		try:
			lc = LoopingCall(self.loopFunction)
			lc.start(1/60)
		except Exception as e:
			print(e)

# run main
if __name__ == '__main__':
	gs = GameSpace()
	gs.start()
