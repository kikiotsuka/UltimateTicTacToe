from __future__ import print_function
import pygame, sys
from pygame.locals import *
from random import randint

"""
INFO
WIDTH = 640
HEIGHT = 740
minibox - 60x60
bigbox - 200x200
"""

class Button:
	def __init__(self, img, loc=(0,0)):
		self.img = img
		self.loc = loc
		self.dim = img.get_size()
		self.box = Rect(loc, self.dim)
	def setloc(self, loc):
		self.loc = loc
		self.box = Rect(loc, self.dim)
	def clicked(self, loc):
		return self.box.collidepoint(loc)

def __main__():
	global board, bigboard, turn, toplace, cpumove
	global xminiimg, ominiimg, xlargeimg, olargeimg, catlargeimg
	global fpsClock
	global window, BLACK, placeboxindicator, BLUE, tiles, tileslarge, WHITE, RED, player1turn, turnbox, turnboxindicator, HEIGHT, cputurn, WIDTH
	global computations, computationslimit
	computationslimit = 50000

	pygame.init()
	fpsClock = pygame.time.Clock()

	WIDTH = 640
	HEIGHT = 740
	window = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption('Tic Tac Toe by Mitsuru Otsuka')

	#images
	olargeimg = pygame.image.load('media/olarge.png')
	xlargeimg = pygame.image.load('media/xlarge.png')
	ominiimg = pygame.image.load('media/omini.png')
	xminiimg = pygame.image.load('media/xmini.png')
	catlargeimg = pygame.image.load('media/catbig.png')
	twoplayerbutton = Button(pygame.image.load('media/twoplayer.png'))
	twoplayerbutton.setloc((WIDTH / 2 - twoplayerbutton.dim[0] / 2, 
							WIDTH // 3.5 - twoplayerbutton.dim[1] / 2 - 50))
	cpubutton = Button(pygame.image.load('media/cpu.png'))
	cpubutton.setloc((WIDTH / 2 - cpubutton.dim[0] / 2, WIDTH // 3.5 * 2 - cpubutton.dim[1] / 2 - 50))
	quitbutton = Button(pygame.image.load('media/quit.png'))
	quitbutton.setloc((WIDTH / 2 - quitbutton.dim[0] / 2, WIDTH // 3.5 * 3 - quitbutton.dim[1] / 2 - 50))
	cpuwin = pygame.image.load('media/cpuwin.png')
	player1win = pygame.image.load('media/player1win.png')
	player2win = pygame.image.load('media/player2win.png')
	draw = pygame.image.load('media/draw.png')
	replay = Button(pygame.image.load('media/replay.png'))
	replay.setloc((WIDTH / 2 - replay.dim[0] / 2, HEIGHT / 2))
	player1turn = pygame.image.load('media/player1turn.png')
	player2turn = pygame.image.load('media/player2turn.png')
	cputurn = pygame.image.load('media/cputurn.png')
	ggwpnore = pygame.image.load('media/ggwpnore.png')

	easybutton = Button(pygame.image.load('media/easy.png'))
	normalbutton = Button(pygame.image.load('media/normal.png'))
	lunaticbutton = Button(pygame.image.load('media/lunatic.png'))
	backbutton = Button(pygame.image.load('media/back.png'))
	easybutton.setloc((WIDTH / 2 - easybutton.dim[0] / 2, WIDTH // 3.5 - easybutton.dim[1] / 2 - 50))
	normalbutton.setloc((WIDTH / 2 - normalbutton.dim[0] / 2, WIDTH // 3.5 * 2 - normalbutton.dim[1] / 2 - 50))
	lunaticbutton.setloc((WIDTH / 2 - lunaticbutton.dim[0] / 2, WIDTH // 3.5 * 3 - lunaticbutton.dim[1] / 2 - 50))
	backbutton.setloc((WIDTH / 2 + 30, lunaticbutton.loc[1] + lunaticbutton.dim[1] + 50))


	#clickable tile locations
	tiles = [[[[0 for x in range(3)] for x in range(3)] for x in range(3)] for x in range(3)]
	tileslarge = [[0 for x in range(3)] for x in range(3)]
	placeboxindicator = [[0 for x in range(3)] for x in range(3)]
	#print(len(tiles))
	ibig=jbig=imini=jmini=0
	for a in range(10, 630 - 20, 210):
		for b in range(10, 630 - 20, 210):
			for x in range(a + 5, a + 200 - 20, 65):
				for y in range(b + 5, b + 200 - 20, 65):
					tiles[ibig][jbig][imini][jmini] = Rect(y, x, 60, 60)
					#print(x, y)
					jmini += 1
				imini += 1
				jmini = 0
			tileslarge[ibig][jbig] = Rect(b, a, 200, 200)
			placeboxindicator[ibig][jbig] = Rect(b - 10, a - 10, 220, 220)
			jbig += 1
			imini = 0
		ibig += 1
		jbig = 0
	
	turnbox = Rect(0, HEIGHT - 97, WIDTH, 97) #space at bottom = 97 px

	#colors
	RED = pygame.Color(255, 0, 0)
	BLUE = pygame.Color(0, 0, 255)
	BLACK = pygame.Color(0, 0, 0)
	WHITE = pygame.Color(255, 255, 255)

	#game states
	menu = True
	playing = False
	gameover = False
	twoplayer = False
	difficultyselect = False
	cpu = False
	winstate = 0

	board = None
	bigboard = None
	turn = None
	turnboxindicator = []
	turnboxindicator.append(Rect(0, HEIGHT + - 97, WIDTH / 2, 97))
	turnboxindicator.append(Rect(WIDTH / 2, HEIGHT - 97, 500, 97))

	toplace = (-1, -1) #if -1, -1 then anywhere, otherwise specific location

	cpumove = None

	while True: #game loop
		if menu:
			window.fill(WHITE)
			window.blit(twoplayerbutton.img, twoplayerbutton.loc)
			window.blit(cpubutton.img, cpubutton.loc)
			window.blit(quitbutton.img, quitbutton.loc)
		elif difficultyselect:
			window.fill(WHITE)
			window.blit(easybutton.img, easybutton.loc)
			window.blit(normalbutton.img, normalbutton.loc)
			window.blit(lunaticbutton.img, lunaticbutton.loc)
			window.blit(backbutton.img, backbutton.loc)
		elif playing:
			window.fill(BLACK)
			#draw move location
			if toplace == (-1, -1):
				for i, a in enumerate(placeboxindicator):
					for j, t in enumerate(a):
						if bigboard[i][j] == 0:
							pygame.draw.rect(window, BLUE, t)
			else:
				pygame.draw.rect(window, BLUE, placeboxindicator[toplace[0]][toplace[1]])
			drawboard(tiles, tileslarge, window, turnbox, board, bigboard)
			pygame.draw.rect(window, WHITE, turnbox)
			if turn:
				pygame.draw.rect(window, RED, turnboxindicator[0])
			else:
				pygame.draw.rect(window, RED, turnboxindicator[1])
			if twoplayer:
				window.blit(player1turn, (5, HEIGHT - 92))
				window.blit(player2turn, (WIDTH / 2 + 5, HEIGHT - 92))
			elif cpu:
				window.blit(player1turn, (5, HEIGHT - 92))
				window.blit(cputurn, (WIDTH / 2 + 5, HEIGHT - 92))
				if not turn: #cpu makes move
					#TODO fixme, also animation sequence?
					pygame.display.update()
					computations = 0
					cpucalculatemove(0, toplace, board, bigboard)
					if cpumove == None:
						x, y = toplace
						while (x, y) == (-1, -1) or bigboard[x][y] != 0:
							x = randint(0, 2)
							y = randint(0, 2)
						i = randint(0, 2)
						j = randint(0, 2)
						while board[x][y][i][j] != 0:
							i = randint(0, 2)
							j = randint(0, 2)
						cpumove = (x, y, i, j)
					winstate = makemove(*cpumove)
					cpumove = None
					if winstate == 1 or winstate == 2:
						playing = False
						gameover = True
		elif gameover:
			window.fill(BLACK)
			drawboard(tiles, tileslarge, window, turnbox, board, bigboard)
			pygame.draw.rect(window, WHITE, turnbox)
			if winstate == 1: #someone won
				if twoplayer:
					if not turn: #player1 won
						window.blit(player1win, (WIDTH / 2 - player1win.get_width() / 2, 100))
					else: #player 2 won
						window.blit(player2win, (WIDTH / 2 - player2win.get_width() / 2, 100))
				else:
					if not turn: #player 1 won
						window.blit(player1win, (WIDTH / 2 - player1win.get_width() / 2, 100))
					else: #cpu won
						window.blit(cpuwin, (WIDTH / 2 - cpuwin.get_width() / 2, 100))
			else: #cat's game
				window.blit(draw, (WIDTH / 2 - draw.get_width() / 2, 100))
			window.blit(replay.img, replay.loc)
			window.blit(ggwpnore, (0, HEIGHT - 97))

		#events
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEBUTTONUP:
				mouseloc = event.pos
				if menu:
					trigger = False
					if twoplayerbutton.clicked(mouseloc):
						trigger = True
						twoplayer = True
					elif cpubutton.clicked(mouseloc):
						difficultyselect = True
						menu = False
					elif quitbutton.clicked(mouseloc):
						pygame.quit()
						sys.exit()
					if trigger:
						menu = False
						playing = True
						board = [[[[0 for x in range(3)] for x in range(3)] for x in range(3)] for x in range(3)]
						bigboard = [[0 for x in range(3)] for x in range(3)]
						turn = turn if turn != None else True if randint(0, 1) == 0 else False
						winstate = 0
				elif difficultyselect:
					trigger = False
					if easybutton.clicked(mouseloc):
						trigger = True
						computationslimit = 40000
					elif normalbutton.clicked(mouseloc):
						trigger = True
						computationslimit = 50000
					elif lunaticbutton.clicked(mouseloc):
						trigger = True
						computationslimit = 60000
					elif backbutton.clicked(mouseloc):
						difficultyselect = False
						menu = True
					if trigger:
						playing = True
						difficultyselect = False
						cpu = True
						board = [[[[0 for x in range(3)] for x in range(3)] for x in range(3)] for x in range(3)]
						bigboard = [[0 for x in range(3)] for x in range(3)]
						turn = turn if turn != None else True if randint(0, 1) == 0 else False
						winstate = 0
						if not turn:
							board[0][0][1][1] = 'o'
							turn = not turn
				elif playing:
					if cpu and not turn:
						continue
					for i, a in enumerate(tiles):
						for j, b in enumerate(a):
							for k, c in enumerate(b):
								for l, t in enumerate(c):
									if t.collidepoint(mouseloc):
										winstate = makemove(i, j, k, l)
										#print(i, j, k, l)
										if winstate == 1 or winstate == 2:
											playing = False
											gameover = True
				else:
					if replay.clicked(mouseloc):
						menu = True
						gameover = False
						cpu = False
						twoplayer = False
		pygame.display.update()
		fpsClock.tick(60)

"""
AI Improvement Ideas

- When AI makes a move, evaluate winning probability at the new grid location
- change heuristics system
	- count number of ways enemy/cpu can win
- RNGeezus
"""

def cpucalculatemove(depth, loc, board, bigboard):
	global cpumove
	global computations, computationslimit
	computations += 1
	maxval = -1000000
	
	#===========================
	global window, BLACK, toplace, placeboxindicator, BLUE, tiles, tileslarge, WHITE, RED, player1turn, turnbox, turnboxindicator, HEIGHT, cputurn, WIDTH
	if computations % 100 == 0:
		window.fill(BLACK)
		#draw move location
		if toplace == (-1, -1):
			for i, a in enumerate(placeboxindicator):
				for j, t in enumerate(a):
					if bigboard[i][j] == 0:
						pygame.draw.rect(window, BLUE, t)
		else:
			pygame.draw.rect(window, BLUE, placeboxindicator[toplace[0]][toplace[1]])
		drawboard(tiles, tileslarge, window, turnbox, board, bigboard)
		pygame.draw.rect(window, WHITE, turnbox)
		pygame.draw.rect(window, RED, turnboxindicator[1])
		window.blit(player1turn, (5, HEIGHT - 92))
		window.blit(cputurn, (WIDTH / 2 + 5, HEIGHT - 92))
		pygame.display.update()
		fpsClock.tick(60)
	#==============================

	if checkwin(bigboard):
		return maxval
	if checkdraw(bigboard):
		return -500000
	if depth == 1000 or computations >= computationslimit:
		return -evaluate(board, 'x')
	for x in range(3):
		for y in range(3):
			for i in range(3):
				for j in range(3):
					if loc == (x, y) or loc == (-1, -1):
						if bigboard[x][y] == 0 and board[x][y][i][j] == 0:
							board[x][y][i][j] = 'o'
							newloc = (i, j)
							addval = 0
							trigger = False
							if checkwin(board[x][y]):
								if bigboard[x][y] != 0:
									toplace = (-1, -1)
								addval += 500000
								bigboard[x][y] = 'o'
								trigger = True
							elif checkdraw(board[x][y]):
								if bigboard[x][y] != 0:
									toplace = (-1, -1)
								bigboard[x][y] = 'c'
								addval += -100000
								trigger = True
							if toplace == (-1, -1):
								addval += -750000
							ans = playercalculatemove(depth + 1, newloc, board, bigboard) + addval
							board[x][y][i][j] = 0
							if trigger:
								bigboard[x][y] = 0
							if ans > maxval:
								maxval = ans
								if depth == 0:
									cpumove = (x, y, i, j)
	return maxval

def playercalculatemove(depth, loc, board, bigboard):
	global computations, computationslimit
	computations += 1
	minval = 1000000
	if checkwin(bigboard):
		return minval
	if checkdraw(bigboard):
		return 500000
	if depth == 1000 or computations >= computationslimit:
		return evaluate(board, 'o')
	for x in range(3):
		for y in range(3):
			for i in range(3):
				for j in range(3):
					if loc == (x, y) or loc == (-1, -1):
						if bigboard[x][y] == 0 and board[x][y][i][j] == 0:
							board[x][y][i][j] = 'x'
							newloc = (i, j)
							addval = 0
							trigger = False
							if checkwin(board[x][y]):
								if bigboard[i][j] != 0:
									newloc = (-1, -1)
								addval += -500000
								bigboard[x][y] = 'x'
								trigger = True
							elif checkdraw(board[x][y]):
								if bigboard[i][j] != 0:
									newloc = (-1, -1)
								bigboard[x][y] = 'c'
								addval += 100000
								trigger = True
							if newloc == (-1, -1):
								addval += 750000
							ans = cpucalculatemove(depth + 1, newloc, board, bigboard) + addval
							board[x][y][i][j] = 0
							if trigger:
								bigboard[x][y] = 0
							if ans < minval:
								minval = ans
	return minval

def evaluate(board, who):
	val = 0
	for a in board:
		for b in a:
			val += evaluatehorz(b, who)
			val += evaluatevert(b, who)
			val += evaluatemindiag(b, who)
			val += evaluatemajdiag(b, who)
	return val


def evaluatehorz(board, who):
	val = 0
	opposite = 'o'
	if who == 'o':
		opposite = 'x'
	for a in board:
		for b in board:
			if b.count(who) == 3:
				val += 30000
			elif b.count(who) == 2 and b.count(0) == 1:
				val += 20000
			elif b.count(who) == 1 and b.count(0) == 2:
				val += 10000
			elif b.count(opposite) == 3:
				val += -30000
			elif b.count(opposite) == 2 and b.count(0) == 1:
				val += -20000
			elif b.count(opposite) == 1 and b.count(0) == 2:
				val += -10000
	return val

def evaluatevert(board, who):
	val = 0
	opposite = 'o'
	if who == 'o':
		opposite = 'x'
	for x in range(0, 3):
		b = [board[j][x] for j in range(3)]
		if b.count(who) == 3:
			val += 30000
		elif b.count(who) == 2 and b.count(0) == 1:
			val += 20000
		elif b.count(who) == 1 and b.count(0) == 2:
			val += 10000
		elif b.count(opposite) == 3:
			val += -30000
		elif b.count(opposite) == 2 and b.count(0) == 1:
			val += -20000
		elif b.count(opposite) == 1 and b.count(0) == 2:
			val += -10000
	return val

def evaluatemindiag(board, who):
	b = []
	for x in range(0, 3):
		b.append(board[x][x])
	opposite = 'o'
	if who == 'o':
		opposite = 'x'
	val = 0
	if b.count(who) == 3:
		val += 30000
	elif b.count(who) == 2 and b.count(0) == 1:
		val += 20000
	elif b.count(who) == 1 and b.count(0) == 2:
		val += 10000
	elif b.count(opposite) == 3:
		val += -30000
	elif b.count(opposite) == 2 and b.count(0) == 1:
		val += -20000
	elif b.count(opposite) == 1 and b.count(0) == 2:
		val += -10000
	return val

def evaluatemajdiag(board, who):
	b = []
	b.append(board[2][0])
	b.append(board[1][1])
	b.append(board[0][2])
	val = 0
	opposite = 'o'
	if who == 'o':
		opposite = 'x'
	if b.count(who) == 3:
		val += 30000
	elif b.count(who) == 2 and b.count(0) == 1:
		val += 20000
	elif b.count(who) == 1 and b.count(0) == 2:
		val += 10000
	elif b.count(opposite) == 3:
		val += -30000
	elif b.count(opposite) == 2 and b.count(0) == 1:
		val += -20000
	elif b.count(opposite) == 1 and b.count(0) == 2:
		val += -10000
	return val

def makemove(i, j, k, l):
	global board, bigboard, turn, toplace
	if bigboard[i][j] == 0 and board[i][j][k][l] == 0 and \
		(toplace == (i, j) or toplace == (-1, -1)):
		if turn:
			board[i][j][k][l] = 'x'
		else:
			board[i][j][k][l] = 'o'
		toplace = (k, l)
		if bigboard[k][l] != 0:
			toplace = (-1, -1)
	else:
		return -1
	if checkwin(board[i][j]):
		if turn:
			bigboard[i][j] = 'x'
		else:
			bigboard[i][j] = 'o'
		if bigboard[k][l] != 0:
			toplace = (-1, -1)
		if checkwin(bigboard):
			turn = not turn
			return 1
		elif checkdraw(bigboard):
			return 2
	elif checkdraw(board[i][j]):
		bigboard[i][j] = 'c'
		if bigboard[k][l] != 0:
			toplace = (-1, -1)
		if checkdraw(bigboard):
			return 2
	if bigboard[k][l] != 0:
		toplace = (-1, -1)
	turn = not turn
	return 0

def drawboard(tiles, tileslarge, window, turnbox, board, bigboard):
	global xminiimg, ominiimg, xlargeimg, olargeimg, catlargeimg
	WHITE = pygame.Color(255, 255, 255)
	#draw tiles
	for a in tiles:
		for b in a:
			for c in b:
				for t in c:
					pygame.draw.rect(window, WHITE, t)
	#draw pieces
	for i, a in enumerate(board):
		for j, b in enumerate(a):
			for k, c in enumerate(b):
				for l, t in enumerate(c):
					if t == 'x':
						window.blit(xminiimg, tiles[i][j][k][l])
					elif t == 'o':
						window.blit(ominiimg, tiles[i][j][k][l])
	#big pieces
	for i, a in enumerate(bigboard):
		for j, t in enumerate(a):
			if t == 'x':
				window.blit(xlargeimg, tileslarge[i][j])
			elif t == 'o':
				window.blit(olargeimg, tileslarge[i][j])
			elif t == 'c':
				window.blit(catlargeimg, tileslarge[i][j])

def checkwin(board):
	return horz(board) or vert(board) or majdiag(board) or mindiag(board)

def horz(board):
	for bl in board:
		if len(set(bl)) == 1 and not ({0, 'c'} & set(bl)):
			return True
	return False

def vert(board):
	for x in range(0, 3):
		arr = [board[j][x] for j in range(3)]
		if len(set(arr)) == 1 and not ({0, 'c'} & set(arr)):
			return True
	return False

def majdiag(board):
	test = []
	for x in range(0, 3):
		test.append(board[x][x])
	return len(set(test)) == 1 and not ({0, 'c'} & set(test))

def mindiag(board):
	return board[2][0]==board[1][1]==board[0][2]!=0

def checkdraw(board):
	for bl in board:
		for b in bl:
			if b == 0:
				return False
	return True

if __name__ == '__main__':
	__main__()