# twistedP1.py
# author: Taylor Rongaus
# due May 1, 2017

# player1 of our two-player Pacman implementation
# see the README for more details on the gameplay
# P1 and P2 are almost indentical code except P1 is the client

import sys, pygame
import Player as p
import Ghost as gh
try:
	from twisted.python import log
	from twisted.internet.protocol import ClientFactory
	from twisted.internet.protocol import Protocol
	from twisted.internet import reactor
	from twisted.internet.task import LoopingCall
except:
	pass

# class for the overall gamespace -- inherit from Protocol
# in order to make it function like a DataConnection class
class GameSpace(Protocol):

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
		self.moveDir = ''
		self.lives = 3
		self.queue = 0
		self.score = 0
		self.ghost_mode = False
		self.time_elapsed = 240
		self.release_time = 719
		self.largeDots = [False, False, False, False]
		pygame.display.set_caption('Pac-Man Player 1')
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
		self.player1 = p.Player(self)
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
		self.connected = 0
		self.opponentScore = ''
		self.opponentEnd = False
		self.sendCount = 0

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

	# cover the necessary dots with black squares
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
	def ingameUpdate(self, numPlayers):
		self.update()
		# blit black over the dots we have covered
		text = "LIVES: "
		text += str(self.lives)
		text2 = "SCORE: "
		text2 += str(self.score)
		self.screen.blit(self.font.render(text, 1, (255,255,255)), (456, 72))
		self.screen.blit(self.font.render(text2, 1, (255,255,255)), (456, 88))
		if numPlayers == 2:
			text3 = "OPPONENT SCORE: "
			if self.opponentScore == 'Waiting for opponent...':
				self.screen.blit(self.font.render(self.opponentScore, 1, (255,255,255)), (456, 120))
			else:
				text3 += str(self.opponentScore)
			self.screen.blit(self.font.render(text3, 1, (255,255,255)), (456, 104))
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
		self.screen.blit(button1, (510, 144))
		self.screen.blit(button2, (510, 184))
		pygame.display.update()
		clicked = False
		main1 = False
		main2 = False		
		# run while a button has not been clicked to start gameplay		
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
			self.opponentScore = 'Waiting for opponent...'
			self.main2()
		else:
			pass

	# function to check to see if we've run over a large dot
	def checkLargeDot(self):
		x = self.player1.rect.centerx
		y = self.player1.rect.centery
		# check to see if we have run over a dot that hasn't yet been run over
		# if so, start "ghost mode"
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
	def reset(self, numPlayers):
		try:
			pygame.mixer.music.load("../sounds/pacman_death.wav")
			pygame.mixer.music.play()
		except:
			print("Error loading ../sounds/pacman_death.wav")
		if self.lives > 0:
			pygame.time.wait(1000)
			self.score = self.score - 100
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
			# if in two player mode and loss occurs, stop the reactor
			if numPlayers == 2:
				reactor.stop()
			self.gameover("YOU LOSE!", numPlayers)
		try:
			pygame.mixer.music.load(self.sound)
			pygame.mixer.music.play(-1)
		except:
			print("Error loading ../sounds/pacman_waka.wav")

	# function to end the game cleanly upon a loss or win and offer play again
	def gameover(self, outcome, numPlayers):
		# determine actual winner in two-player scenario
		outcome2 = ''
		if numPlayers == 2:
			if outcome == "YOU WON!":
				if self.opponentEnd == True:
					if int(self.opponentScore) > self.score:
						suppl
						outcome = "YOU LOST!"
						outcome2 = "The opponent scored more points than you"
					elif int(self.opponentScore) == self.score:
						outcome = "YOU LOST!"
						outcome2 = "The opponent had the same score as you but finished first"
		if outcome == "YOU WON!":
			try:
				pygame.mixer.music.load("../sounds/ta-da.wav")
				pygame.mixer.music.play()
			except:
				print("Error loading ../sounds/ta-da.wav")
		# load in the end screen
		self.screen.fill(self.black)
		text = outcome
		self.screen.blit(self.font.render(text, 1, (255,255,255)), (self.width/2-20, self.height/2-60))
		if numPlayers != 2:
			text2 = " Play again?"
			text3 = "1 PLAYER"
			text4 = "2 PLAYER"
			pygame.draw.rect(self.screen, (255,255,255), (self.width/2-32, self.height/2,100,30))
			pygame.draw.rect(self.screen, (255,255,255), (self.width/2-32, self.height/2+50,100,30))
			self.screen.blit(self.font.render(text2, 1, (255,255,255)), (self.width/2-20, self.height/2-30))
			self.screen.blit(self.font.render(text3, 1, (0,0,0)), (self.width/2-15, self.height/2+8))
			self.screen.blit(self.font.render(text4, 1, (0,0,0)), (self.width/2-15, self.height/2+58))
		else:
			self.screen.blit(self.font.render(outcome2, 1, (255,255,255)), (self.width/2-80, self.height/2-30))
		pygame.display.update()	
		clicked = False
		main1 = False
		main2 = False
		# run while the player hasn't clicked on either of the buttons
		while not clicked:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					# for some reason throws a Deferred error but 
					# we already have stopped the reactor...?
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					pos = pygame.mouse.get_pos()
					# determine if user clicked w/in the range of either of the start buttons
					if pos[0] >= self.width/2-40 and pos[0] <= self.width/2+60:
						if pos[1] >= self.height/2 and pos[1] <= self.height/2+30:
							clicked = True
							main1 = True
						if numPlayers != 2:
							if pos[1] >= self.height/2+50 and pos[1] <= self.height/2+80:
								clicked = True
								main2 = True
		# restart the game and re-initialize the gamespace
		self.__init__()
		if main1 == True:
			self.main1()
		elif main2 == True:
			self.opponentScore = '0'
			self.main2()
		else: 
			pass

	# main1 begins once we press the player 1 start button
	# we separated main1 from main2 b/c we didn't want to accidentally
	# break a well-working one-player game by adding in two-player
	def main1(self):
		pygame.key.set_repeat(1,100)
		# need to figure out how to add in the proper sound effects
		try:
			pygame.mixer.music.load(self.sound)
			pygame.mixer.music.play(-1)
		except:
			print("Error loading ../sounds/pacman_waka.wav")
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
							self.moveDir = 'left'
							self.queue = 1
						else:
							self.queue = 1
					elif event.key == pygame.K_RIGHT:
						if self.board[y][x + 1] == '1':
							self.moveDir = 'right'
							self.queue = 2
						else:
							self.queue = 2
					elif event.key == pygame.K_UP:
						if self.board[y - 1][x] == '1':
							self.moveDir = 'up'
							self.queue = 3
						else:
							self.queue = 3
					elif event.key == pygame.K_DOWN:
						if self.board[y + 1][x] == '1':
							self.moveDir = 'down'
							self.queue = 4
						else:
							self.queue = 4
			# check the self queue to see what arrows the player has pressed
			if self.queue == 1 and self.board[y][x - 1] == '1':
				self.moveDir = 'left'
			elif self.queue == 2 and self.board[y][x + 1] == '1':
				self.moveDir = 'right'
			elif self.queue == 3 and self.board[y - 1][x] == '1':
				self.moveDir = 'up'
			elif self.queue == 4 and self.board[y + 1][x] == '1':
				self.moveDir = 'down'
			# move the pac and update the changes to the screen
			if self.player1.move(self) == True:
				self.score = self.score + 10
			self.ingameUpdate(1)
			# check to see if we've run over a large dot
			self.checkLargeDot()
			# check to see if we have collided with a ghost
			if self.ghost_mode == False:
				if (self.player1.rect.colliderect(self.red_ghost.rect) or self.player1.rect.colliderect(self.blue_ghost.rect)) or self.player1.rect.colliderect(self.pink_ghost.rect) or self.player1.rect.colliderect(self.orange_ghost.rect):
					self.lives -= 1
					self.reset(1)
			# check to see if we have won
			if self.checkWin() == True:
				self.gameover("YOU WON!", 1)
			# update the screen
			pygame.display.flip()

	# function to hold the stuff in the while loop for two-player
	def loopFunction(self):
		self.sendCount += 1
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
				reactor.stop()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					if self.board[y][x - 1] == '1':
						self.moveDir = 'left'
						self.queue = 1
					else:
						self.queue = 1
				elif event.key == pygame.K_RIGHT:
					if self.board[y][x + 1] == '1':
						self.moveDir = 'right'
						self.queue = 2
					else:
						self.queue = 2
				elif event.key == pygame.K_UP:
					if self.board[y - 1][x] == '1':
						self.moveDir = 'up'
						self.queue = 3
					else:
						self.queue = 3
				elif event.key == pygame.K_DOWN:
					if self.board[y + 1][x] == '1':
						self.moveDir = 'down'
						self.queue = 4
					else:
						self.queue = 4
		# check the self queue to see what arrows the player has pressed
		if self.queue == 1 and self.board[y][x - 1] == '1':
			self.moveDir = 'left'
		elif self.queue == 2 and self.board[y][x + 1] == '1':
			self.moveDir = 'right'
		elif self.queue == 3 and self.board[y - 1][x] == '1':
			self.moveDir = 'up'
		elif self.queue == 4 and self.board[y + 1][x] == '1':
			self.moveDir = 'down'
		# move the pac and update the changes to the screen
		if self.player1.move(self) == True:
			self.score = self.score + 10		
		self.ingameUpdate(2)
		# check to see if we've run over a large dot
		self.checkLargeDot()
		# check to see if we have collided with a ghost 
		if self.ghost_mode == False:
			if (self.player1.rect.colliderect(self.red_ghost.rect) or self.player1.rect.colliderect(self.blue_ghost.rect)) or self.player1.rect.colliderect(self.pink_ghost.rect) or self.player1.rect.colliderect(self.orange_ghost.rect):
				self.lives -= 1
				self.reset(2)
		# check to see if we have won
		if self.checkWin() == True:
			self.gameover("YOU WON!", 2)
			self.transport.write('end')

		# send over the player's score  
		# use % to slow this down a bit
		if self.sendCount % 2 == 0:
			self.transport.write(str(self.score))
		# update the screen
		pygame.display.flip()

	# main begins once we press the start button
	def main2(self):
		pygame.key.set_repeat(1,100)
		try:
			pygame.mixer.music.load(self.sound)
			pygame.mixer.music.play(-1)
		except:
			print("Error loading ../sounds/pacman_waka.wav")
		# create the data factory and make the connection
		self.datafact = DataFactory()
		reactor.connectTCP("ash.campus.nd.edu", 41097, self.datafact)
		# start the looping call on the loop function 
		# display waiting text until connection is made		
		self.screen.fill(self.black)
		text = "Waiting for opponent..."
		self.screen.blit(self.font.render(text, 1, (255,255,255)), (self.width/2-60, self.height/2))
		pygame.display.update()		
		reactor.run()

	# functions for the data connection   
	def connectionMade(self):
		self.transport.write(str(self.score))
		lc = LoopingCall(self.loopFunction)
		lc.start(1/60)

	def dataReceived(self, data):
		if data != 'end':
			if self.opponentScore != data:
				self.opponentScore = data
				self.ingameUpdate(2)
		else:
			self.opponentEnd = True

# class for the DataFactory that is instantiated in main2

class DataFactory(ClientFactory):
   
	def __init__(self):
		self.myconn = GameSpace()

	def buildProtocol(self, addr):
		return self.myconn

# run the main execution
if __name__ == '__main__':
	#log.startLogging(sys.stdout)
	gs = GameSpace()
	gs.start()
