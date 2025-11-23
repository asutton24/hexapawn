import pygame
from hexapawn import Hexapawn, HexAI


WIDTH = 1600
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

def drawMoves(screen, moves):	
	boxSize = HEIGHT // SCALING
	originx = WIDTH // 2 - boxSize
	originy = HEIGHT // 2 - boxSize
	lineThickness = boxSize // 20
	colors=[(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
	colorI = 0
	
	for m in moves:
		start = (m[0][0] * boxSize + originx, m[0][1] * boxSize + originy)
		end = (m[1][0] * boxSize + originx, m[1][1] * boxSize + originy)
		pygame.draw.line(screen, colors[colorI], start, end, int(lineThickness))
		colorI += 1

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
	
	viewMoves = False

	viewWait = True

	while running:
		clock.tick(60)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					if game.turn == "white" or mode == "manual":
						tiles.append(getClickedTile(event.pos[0], event.pos[1]))
					viewWait = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r:
					game = Hexapawn()
					ai.game = game
					viewWait = False
				elif event.key == pygame.K_t:
					if mode == "train":
						mode = "auto"
					else:
						mode = "train"
				elif event.key == pygame.K_h:
					game.printGame()
				elif event.key == pygame.K_v:
					viewMoves = not viewMoves
					viewWait = game.turn == 'black'
				elif event.key == pygame.K_SPACE:
					viewWait = False
				elif event.key == pygame.K_f:
					ai.forbidden = {}
					ai.totalForbidden = 0
				elif event.key == pygame.K_s:
					if mode == "manual":
						mode = "auto"
					else:
						mode = "manual"
		if viewMoves and viewWait:
			pass
		elif game.winner != 0:
			if game.winner == -1:
				print("Player win")
				print("Total forbidden Moves: ", ai.totalForbidden)
				game.winner = -2
			elif game.winner == 1:
				#print("CPU Win")
				#print("Total forbidden Moves: ", ai.totalForbidden)
				game.winner = 2
			if mode == "train":
				game = Hexapawn()
				ai.game = game
			tiles = []
		elif game.turn == 'white' and len(tiles) == 2 and mode in ["auto", "manual"]:
			game.doMove(tiles[0], tiles[1])
			game.updateWinner()
			if game.winner == -1 and mode == "auto":
				ai.updateForbidden()
				viewWait = False
			else:
				viewWait = mode == "auto"
			tiles = []
		elif game.turn == 'white' and mode == "train":
			ai.autoPlayWhite()
			if game.winner == -1:
				ai.updateForbidden()
		elif game.turn == 'black' and mode == 'manual' and len(tiles) == 2:
			game.doMove(tiles[0], tiles[1])
			game.updateWinner()
			tiles = []
			viewWait = False
		elif game.turn == 'black' and mode in ["auto", "train"]:
			ai.makeMove() 
			game.updateWinner()
			viewWait = False
		screen.fill((0, 0, 0))
		drawBoard(screen)
		if viewMoves and game.turn == 'black' and game.winner == 0:
			drawMoves(screen, ai.getValidMoves())
		drawPawns(screen, game.getStateString())
		pygame.display.update()

main()
