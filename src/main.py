# main.py
# authors: Taylor Rongaus & Henry Long

import sys, pygame
import Player1 as p1
import Ghost as gh

class GameSpace:

	def __init__(self):
		pygame.init()
		self.size = self.width, self.height = 640, 496
		self.black = 0,0,0
		self.screen = pygame.display.set_mode(self.size)
		self.image = pygame.image.load("../img/full-board.png")
		self.image = pygame.transform.scale2x(self.image)
		pygame.display.set_caption('Pac-Man')
		self.rect = self.image.get_rect()
		self.rect.centerx = 224 
		self.rect.centery = 248
		self.clock = pygame.time.Clock()
		self.player1 = p1.Player1(self)
		self.red_ghost = gh.Ghost(self,"ghost-red-up.png")
		self.red_ghost.rect.centery -= 42
		self.blue_ghost = gh.Ghost(self, "ghost-blue-up.png")
		self.blue_ghost.rect.centerx += 30
		self.pink_ghost = gh.Ghost(self, "ghost-pink-up.png")
		self.pink_ghost.rect.centerx -= 30
		self.orange_ghost = gh.Ghost(self, "ghost-orange-up.png")

	def main(self):
		while 1:
			# clock tick
			self.clock.tick(60)
			# see if any new events have occurred
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LEFT:
						print("K_LEFT")
					elif event.key == pygame.K_RIGHT:
						print("K_RIGHT")
					elif event.key == pygame.K_UP:
						print("K_UP")
					elif event.key == pygame.K_DOWN:
						print("K_DOWN")

			# update the screen
			self.screen.fill(self.black)
			self.screen.blit(self.image, self.rect)
			self.screen.blit(self.player1.image, self.player1.rect)
			self.screen.blit(self.red_ghost.image, self.red_ghost.rect)
			self.screen.blit(self.blue_ghost.image, self.blue_ghost.rect)
			self.screen.blit(self.pink_ghost.image, self.pink_ghost.rect)
			self.screen.blit(self.orange_ghost.image, self.orange_ghost.rect)
			pygame.display.flip()

# run main
if __name__ == '__main__':
	gs = GameSpace()
	gs.main()