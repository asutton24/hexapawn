import pygame
from hexapawn import Hexapawn, HexAI
import cairosvg
import io

pygame.init()

WIDTH, HEIGHT = desktop_width, desktop_height = pygame.display.get_desktop_sizes()[0]
SCALING = 3.5

with open("wpawn.svg", "rb") as f:
	wdata = f.read()
	f.close()
with open("bpawn.svg", "rb") as f:
	bdata = f.read()
	f.close()
wbytes = cairosvg.svg2png(bytestring=wdata, output_width= HEIGHT // SCALING, output_height= HEIGHT // SCALING)
bbytes = cairosvg.svg2png(bytestring=bdata, output_width= HEIGHT // SCALING, output_height= HEIGHT // SCALING)
whitePawn = pygame.image.load(io.BytesIO(wbytes), "wpawn.png")
blackPawn = pygame.image.load(io.BytesIO(bbytes), "bpawn.png")


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
	originx = WIDTH // 2 - (boxSize * 3 // 2)
	originy = HEIGHT // 2 - (boxSize * 3 // 2)
	x = 0
	y = 0

	for c in state:
		if c == 'B':
			screen.blit(blackPawn, (originx + x * boxSize, originy + y * boxSize))
		if c == 'W':
			screen.blit(whitePawn, (originx + x * boxSize, originy + y * boxSize))
		x += 1
		if x == 3:
			x = 0
			y += 1

def drawMoves(screen, moves, allMoves):	
	boxSize = HEIGHT // SCALING
	originx = WIDTH // 2 - boxSize
	originy = HEIGHT // 2 - boxSize
	lineThickness = boxSize // 20
	colors=[(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
	colorI = 0
	
	for m in allMoves:
		if not (m in moves):
			colorI += 1
			continue
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

	screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
	clock = pygame.time.Clock()
	running = True
	tiles = []

	game = Hexapawn()
	ai = HexAI()
	ai.game = game
	
	mode = 'auto'
	
	viewMoves = False

	viewWait = True

	potential = False

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
				elif event.key == pygame.K_q:
					running = False
				elif event.key == pygame.K_p:
					potential = not potential
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
			if potential:
				drawMoves(screen, ai.getPossibleMoves(), ai.getPossibleMoves())
			else:
				drawMoves(screen, ai.getValidMoves(), ai.getPossibleMoves())
		drawPawns(screen, game.getStateString())
		pygame.display.update()

main()
