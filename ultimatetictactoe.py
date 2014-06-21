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
					pygame.display.update()
					#cpucalculatemove(0, toplace, board, bigboard)
					if cpumove != None:
						print('ALL ACCORDING TO KEIKAKU')
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
						cpumove = (i, j)
					cpufinalmove = toplace + cpumove
					winstate = makemove(*cpufinalmove)
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
						trigger = True
						cpu = True
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
					if cpu:
						if not turn:
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

def cpucalculatemove(depth, loc, board, bigboard):
	global cpumove
	pygame.display.update()
	if checkwin(bigboard):
		return -1000
	if checkdraw(bigboard):
		return 0
	if depth == 5:
		return evaluate(board, 'o')
	maxval = -999
	for i in range(3):
		for j in range(3):
			if board[loc[0]][loc[1]][i][j] == 0:
				board[loc[0]][loc[1]][i][j] = 'o'
				newloc = (i, j)
				trigger = False
				if checkwin(board[loc[0]][loc[1]]):
					bigboard[loc[0]][loc[1]] = 'o'
					trigger = True
				elif checkdraw(board[loc[0]][loc[1]]):
					bigboard[loc[0]][loc[1]] = 'c'
					trigger = True
				ans = playercalculatemove(depth + 1, newloc, board, bigboard)
				board[loc[0]][loc[1]][i][j] = 0
				if trigger:
					bigboard[loc[0]][loc[1]] = 0
				if ans > maxval:
					if depth == 0:
						cpumove = (i, j)
	return maxval

def playercalculatemove(depth, loc, board, bigboard):
	if checkwin(bigboard):
		return 1000
	if checkdraw(bigboard):
		return 0
	if depth == 5:
		return evaluate(board, 'x')
	minval = 999
	for i in range(3):
		for j in range(3):
			if board[loc[0]][loc[1]][i][j] == 0:
				newloc = (i, j)
				board[loc[0]][loc[1]][i][j] = 'x'
				trigger = False
				if checkwin(board[loc[0]][loc[1]]):
					bigboard[loc[0]][loc[1]] = 'o'
					trigger = True
				elif checkdraw(board[loc[0]][loc[1]]):
					bigboard[loc[0]][loc[1]] = 'c'
					trigger = True
				ans = cpucalculatemove(depth + 1, newloc, board, bigboard)
				if trigger:
					bigboard[loc[0]][loc[1]] = 0
				board[loc[0]][loc[1]][i][j] = 0
				if ans < minval:
					minval = ans
	return minval

def evaluate(board, who):
	val = 0
	for a in board:
		for b in a:
			if checkwin(b):
				val += 100
			if checkdraw(b):
				val += -10
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
			if b.count(opposite) == 0 and b.count(who) == 2:
				val += 50
			elif b.count(opposite) == 1:
				val += -3
			elif b.count(opposite) == 2:
				val += -10
	return val

def evaluatevert(board, who):
	val = 0
	opposite = 'o'
	if who == 'o':
		opposite = 'x'
	for x in range(0, 3):
		b = [board[j][x] for j in range(3)]
		if b.count(opposite) == 0 and b.count(who) == 2:
			val += 50
		elif b.count(opposite) == 1:
			val += -3
		elif b.count(opposite) == 2:
			val += -10
	return val

def evaluatemindiag(board, who):
	b = []
	for x in range(0, 3):
		b.append(board[x][x])
	opposite = 'o'
	if who == 'o':
		opposite = 'x'
	val = 0
	if b.count(opposite) == 0 and b.count(who) == 2:
		val += 50
	elif b.count(opposite) == 1:
		val += -3
	elif b.count(opposite) == 2:
		val += -10
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
	if b.count(opposite) == 0 and b.count(who) == 2:
		val += 50
	elif b.count(opposite) == 1:
		val += -3
	elif b.count(opposite) == 2:
		val += -10
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
		#TODO FIX ME
		return 0
	if checkwin(board[i][j]):
		if turn:
			bigboard[i][j] = 'x'
		else:
			bigboard[i][j] = 'o'
		toplace = (-1, -1)
		if checkwin(bigboard):
			turn = not turn
			return 1
		elif checkdraw(bigboard):
			return 2
	elif checkdraw(board[i][j]):
		bigboard[i][j] = 'c'
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