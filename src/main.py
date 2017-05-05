# main.py
# authors: Taylor Rongaus & Henry Long

import sys, pygame
import Player1 as p1
import Ghost as gh

class GameSpace:

	# main gamsepace and sprites initialization
	def __init__(self):
		pygame.init()
		self.clock = pygame.time.Clock()
		self.sound = "../sounds/pacman_chomp.wav"
		self.size = self.width, self.height = 640, 496
		self.black = 0,0,0
		self.black_square = pygame.transform.scale2x(pygame.image.load("../img/black-square.png"))
		self.screen = pygame.display.set_mode(self.size)
		self.board = [[]]
		self.readBoard()
		self.travelled = [[]]
		self.readTravelled()
		self.lives = 3
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

	# run this function until the start button is pressed
	def start(self):
		clicked = False
		# pygame.mixer.music.load("../sounds/pacman_beginning.wav")
		# pygame.mixer.music.play()
		self.update()
		# update the screen with the directions and start button
		pygame.draw.rect(self.screen, (255,255,255), (494,140,100,30))
		text1 = "Use the arrow keys to move,"
		text2 = "eat all the dots and"
		text3 = "avoid the ghosts."
		text4 = "PLAY"
		directions = self.font.render("DIRECTIONS:", 1, (255,255,255))
		directions1 = self.font.render(text1, 1, (255,255,255))
		directions2 = self.font.render(text2, 1, (255,255,255))
		directions3 = self.font.render(text3, 1, (255,255,255))
		button1 = self.font.render(text4, 1, (0,0,0))
		self.screen.blit(directions, (500, 56))
		self.screen.blit(directions1, (452, 72))
		self.screen.blit(directions2, (452, 88))
		self.screen.blit(directions3, (452, 104))
		self.screen.blit(button1, (526, 144))
		pygame.display.update()			
		while not clicked:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					pos = pygame.mouse.get_pos()
					# determine if user clicked w/in the range of the start button
					if pos[0] >= 494 and pos[0] <= 594:
						if pos[1] >= 140 and pos[1] <= 170:
							clicked = True
		self.main()

	# main begins once we press the start button
	def main(self):
		pygame.key.set_repeat(1,100)
		# need to figure out how to add in the proper sound effects
		#pygame.mixer.music.load(self.sound)
		#pygame.mixer.music.play(-1)
		while 1:
			# clock tick
			self.clock.tick(60)
			self.red_ghost.move(self, 'red')
			self.blue_ghost.move(self, 'blue')
			self.pink_ghost.move(self, 'pink')
			self.orange_ghost.move(self, 'orange')
			# see if any new events have occurred
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LEFT:
						self.player1.move(self, 'left')
					elif event.key == pygame.K_RIGHT:
						self.player1.move(self, 'right')
					elif event.key == pygame.K_UP:
						self.player1.move(self, 'up')
					elif event.key == pygame.K_DOWN:
						self.player1.move(self, 'down')
			# check to see if we have collided with a ghost
			if (self.player1.rect.colliderect(self.red_ghost.rect) or self.player1.rect.colliderect(self.blue_ghost.rect)) or self.player1.rect.colliderect(self.pink_ghost.rect) or self.player1.rect.colliderect(self.orange_ghost.rect):
				self.lives -= 1
				self.reset()
			# check to see if we have won
			if self.checkWin() == True:
				self.gameWin()
			# update the screen
			self.ingameUpdate()
			pygame.display.flip()

	# function to iterate through the travelled board and determine if the player has won
	def checkWin(self):
		print("ENTERED")
		i=0
		j=0
		x = True
		for row in self.travelled:
			i = i + 1
			for col in row:
				j = j + 1
				if col == '1':
					print(i,j)
					x = False
			j = 0
		return x

	# function to reset the board after a life is lost
	def reset(self):
		if self.lives > 0:
			pygame.time.wait(1000)
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
			self.gameover()

	# function to end the game cleanly upon a loss
	def gameover(self):
		self.screen.fill(self.black)
		text = "GAME OVER"
		self.screen.blit(self.font.render(text, 1, (255,255,255)), (self.width/2-20, self.height/2))
		pygame.display.update()	
		pygame.time.wait(5000)
		sys.exit()

	# function to end the game cleanly upon a win
	def gameWin(self):
		self.screen.fill(self.black)
		text = "YOU WIN!"
		self.screen.blit(self.font.render(text, 1, (255,255,255)), (self.width/2-20, self.height/2))
		pygame.display.update()	
		pygame.time.wait(5000)
		sys.exit()

# run main
if __name__ == '__main__':
	gs = GameSpace()
	gs.start()
