import random

class Pawn:

	def __init__(self, x, y, color):
		self.x = x
		self.y = y
		self.color = color
		self.lastx = x
		self.lasty = y
	
	def move(self, moveType):
		self.lasty = self.y
		self.lastx = self.x
		if self.color == "black":
			self.y += 1
		else:
			self.y -= 1
		if moveType == "l":
			self.x -= 1
		elif moveType == "r":
			self.x += 1
	
	def revert(self):
		self.x = self.lastx
		self.y = self.lasty
	
	def clear(self):
		self.lastx = self.x
		self.lasty = self.y

	def atSamePosition(self, other):
		return self.x == other.x and self.y == other.y

	def isAtPosition(self, pos):
		return self.x == pos[0] and self.y == pos[1]
	
	def inBounds(self):
		return (0 <= self.x <= 2) and (0 <= self.y <= 2)
	
	def getPosTuple(self):
		return (self.x, self.y)

class Hexapawn:
	
	def __init__(self):
		self.turn = "white"
		self.wpawns = []
		self.bpawns = []
		for i in range(3):
			self.wpawns.append(Pawn(i, 2, "white"))
			self.bpawns.append(Pawn(i, 0, "black"))
		self.winner = 0

	def pawnAt(self, pos):
		for p in self.wpawns:
			if p.isAtPosition(pos):
				return True
		for p in self.bpawns:
			if p.isAtPosition(pos):
				return True
		return False
		
	def getPawnAt(self, pos):
		for p in self.wpawns:
			if p.isAtPosition(pos):
				return p
		for p in self.bpawns:
			if p.isAtPosition(pos):
				return p
		return None

	def removePawnAt(self, pos):
		for p in self.wpawns:
			if p.isAtPosition(pos):
				self.wpawns.remove(p)
				return
		for p in self.bpawns:
			if p.isAtPosition(pos):
				self.bpawns.remove(p)
				return
		
	def move(self, start, target, probe):
		if (not self.pawnAt(start)) or self.getPawnAt(start).color != self.turn:
			return False
		if (self.turn == "white" and start[1] - target[1] != 1) or (self.turn == "black" and target[1] - start[1] != 1): 
				return False
		if start[0] == target[0]:
			if self.pawnAt(target):
				return False
			movedPawn = self.getPawnAt(start)
			movedPawn.move("f")
			if not movedPawn.inBounds():
				movedPawn.revert()
				return False
			if probe:
				movedPawn.revert()
			return True
		if start[0] - target[0] == 1:
			if (not self.pawnAt(target)) or (self.getPawnAt(target).color == self.turn):
				return False
			if not probe:
				self.removePawnAt(target)
				self.getPawnAt(start).move("l")
			return True
		if start[0] - target[0] == -1:
			if (not self.pawnAt(target)) or (self.getPawnAt(target).color == self.turn):
				return False
			if not probe:
				self.removePawnAt(target)
				self.getPawnAt(start).move("r")
			return True
		return False
	
	def doMove(self, start, target):
		ret = self.move(start, target, False)
		if self.turn == "black":
			self.turn = "white"
		else:
			self.turn = "black"
		return ret
		
	def probeMove(self, start, target):
		return self.move(start, target, True)

	def updateWinner(self):
		if len(self.wpawns) == 0:
			self.winner = 1
		elif len(self.bpawns) == 0:
			self.winner = -1
		else:
			for p in self.wpawns:
				if p.y == 0:
					self.winner = -1
					return
			for p in self.bpawns:
				if p.y == 2:
					self.winner = 1
					return
			if self.turn == "white":
				pawns = self.wpawns
				winval = 1
			else:
				pawns = self.bpawns
				winval = -1
			movesExist = False
			for p in pawns:
				for i in range(-1, 2):
					movesExist = movesExist or self.probeMove((p.x, p.y), (p.x + i, p.y - winval))
			if not movesExist:
				self.winner = winval
	
	def getStateString(self):
		ret = ''
		for i in range(3):
			for j in range(3):
				if self.pawnAt((j, i)):
					ret += self.getPawnAt((j, i)).color[0].upper()
				else:
					ret += 'X'
		return ret

class HexAI:
	
	def __init__(self):
		self.forbidden = {}
		self.lastMove = None
		self.game = None

	def getPossibleMoves(self):
		moves = []
		for p in self.game.bpawns:
			for i in range(-1, 2):
				if self.game.probeMove((p.x, p.y), (p.x + i, p.y + 1)):
					moves.append(((p.x, p.y), (p.x + i, p.y + 1)))
		return moves

	def getValidMoves(self):
		moves = self.getPossibleMoves()
		return [m for m in moves if not m in self.forbidden.get(self.game.getStateString(), [])]

	def makeMove(self):
		if self.game.turn == "white":
			return False
		moves = self.getValidMoves(self)
		if len(moves) == 0:
			return False
		curMove = random.choice(moves)
		self.game.doMove(curMove[0], curMove[1])
		self.game.updateWinner()
		self.lastMove = [self.game.getStateString(), curMove]
		return True

	def updateForbidden(self):
		if self.forbidden.get(self.lastMove[0]) == None:
			self.forbidden[self.lastMove[0]] = [self.lastMove[1]]
		else:
			self.forbidden[self.lastMove[0]].append(self.lastMove[1])

			
def prettyPrint(h):
	s = h.getStateString()
	s = s.replace("X", " ")
	for i in range(3):
		print(s[(3*i):(3*i+3)])

h = Hexapawn()

ai = HexAI()
ai.game = h

h.doMove((1,2),(1,1))
print(ai.getValidMoves())
prettyPrint(h)
