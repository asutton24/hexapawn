import pygame
from hexapawn import Hexapawn, HexAI


WIDTH = 320
HEIGHT = WIDTH * 9 / 16
SCALING = 3.5

def drawBoard(screen):
	boxSize = HEIGHT // SCALING
	originx = WIDTH // 2 - (boxSize * 3 // 2)
	originy = HEIGHT // 2 - (boxSize * 3 // 2)
	colors = [(255, 206, 158), (209, 139, 71)]
	colorI = 0
	for y in range(3):
		for x in range(3):
			pygame.draw.rect(screen, colors[colorI % 2], (originx + x * boxSize, originy + y * boxSize, boxSize, boxSize))
			colorI += 1

def drawPawns(screen, state):
	radius = HEIGHT // (SCALING * 2.7)
	boxSize = HEIGHT // SCALING
	originx = WIDTH // 2 - boxSize
	originy = HEIGHT // 2 - boxSize
	x = 0
	y = 0

	for c in state:
		if c == 'B':
			pygame.draw.circle(screen, (0, 0, 0), (originx + x * boxSize, originy + y * boxSize), radius, 0)
		if c == 'W':
			pygame.draw.circle(screen, (255, 255, 255), (originx + x * boxSize, originy + y * boxSize), radius, 0)
		x += 1
		if x == 3:
			x = 0
			y += 1

def getClickedTile(mx, my):
	boxSize = HEIGHT // SCALING
	originx = WIDTH // 2 - (boxSize * 3 // 2)
	originy = HEIGHT // 2 - (boxSize * 3 // 2)
	mx = (mx - originx) // boxSize
	my = (my - originy) // boxSize
	if 0 <= mx <= 2 and 0 <= my <= 2:
		return (mx, my)
	return None

def main():
	pygame.init()

	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	clock = pygame.time.Clock()
	running = True
	tiles = []

	game = Hexapawn()
	ai = HexAI()
	ai.game = game
	
	mode = 'auto'

	while running:
		clock.tick(60)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					tiles.append(getClickedTile(event.pos[0], event.pos[1]))
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r:
					game = Hexapawn()
					ai.game = game
		if game.winner != 0:
			tiles = []
		elif game.turn == 'white' and len(tiles) == 2:
			game.doMove(tiles[0], tiles[1])
			game.updateWinner()
			if game.winner == -1 and mode == 'auto':
				ai.updateForbidden()
			tiles = []
		elif game.turn == 'black' and mode == 'manual' and len(tiles) == 2:
			game.doMove(tiles[0], tiles[1])
			game.updateWinner()
			tiles = []
		elif game.turn == 'black' and mode == 'auto':
			ai.makeMove() 
			game.updateWinner()
		screen.fill((0, 0, 0))
		drawBoard(screen)
		drawPawns(screen, game.getStateString())
		pygame.display.update()

main()
