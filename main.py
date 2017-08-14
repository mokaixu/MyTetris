#Monica's Attemp at coding python

import random, time, pygame, sys 
from pygame.locals import *

# SETUP CONSTANTS
FPS = 25
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BOXSIZE = 20
NUMBOXWIDTH = 10
NUMBOXHEIGHT = 20
BLANK = '.'
MOVESIDEWAYSFREQ = 0.10 #when L/R keys are pressed, will move 0.15 boxes per second
MOVEDOWNFREQ = 0.1 #when down key is pressed, will move 0.1 boxes down per second

XMARGIN = int((WINDOWWIDTH - NUMBOXWIDTH * BOXSIZE) / 2)
TOPMARGIN = WINDOWHEIGHT - (NUMBOXHEIGHT * BOXSIZE) - 5

# COLOR CONSTANTS
WHITE = (255, 255, 255)
GRAY = (185, 185, 185)
BLACK = (0, 0, 0)
RED = (255, 0, 170)
GREEN = (170, 255, 0)
BLUE = (0, 170, 255)
PURPLE = (170, 0, 255)

BORDERCOLOR = BLUE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
COLORS = (BLUE, GREEN, RED, PURPLE)

# TEMPLATE PIECES
TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

#Note: Python interpreter ignores tabbing errors inside lists

S_TEMPLATE = [
	['.....',
	 '.....',
	 '..OO.',
	 '.OO..',
	 '.....'],
	['.....',
	 '.O...',
	 '.OO..',
	 '..O..',
	 '.....']
]

Z_TEMPLATE = [
	['.....',
	 '.....',
	 '.OO..',
	 '..OO.',
	 '.....'],
	['.....',
	 '..O..',
	 '.OO..',
	 '.O...',
	 '.....']
]

I_TEMPLATE = [
	['..O..',
	 '..O..',
	 '..O..',
	 '..O..',
	 '.....'],
	['.....',
	 '.....',
	 '.OOOO',
	 '.....',
	 '.....']
]

O_TEMPLATE = [
	['.....',
	 '.....',
	 '.OO..',
	 '.OO..',
	 '.....']]

L_TEMPLATE = [['.....',
                '...O.',
                '.OOO.',
                '.....',
                '.....'],
                ['.....',
                 '..O..',
                 '..O..',
                 '..OO.',
                 '.....'],
                     ['.....',
                      '.....',
                      '.OOO.',
                      '.O...',
                      '.....'],
                     ['.....',
                      '.OO..',
                      '..O..',
                      '..O..',
                      '.....']]

T_TEMPLATE = [['.....',
               '..O..',
                      '.OOO.',
                      '.....',
                      '.....'],
                     ['.....',
                      '..O..',
                      '..OO.',
                      '..O..',
                      '.....'],
                     ['.....',
                      '.....',
                      '.OOO.',
                      '..O..',
                      '.....'],
                     ['.....',
                      '..O..',
                      '.OO..',
                      '..O..',
                     '.....']]
J_TEMPLATE = [['.....',
                       '.O...',
                       '.OOO.',
                       '.....',
                       '.....'],
                      ['.....',
                       '..OO.',
                       '..O..',
                       '..O..',
                       '.....'],
                      ['.....',
                       '.....',
                       '.OOO.',
                       '...O.',
                      '.....'],
                     ['.....',
                      '..O..',
                      '..O..',
                      '.OO..',
                      '.....']]

# All Shape Data
SHAPES = {'S': S_TEMPLATE,
'Z': Z_TEMPLATE, 
'J': J_TEMPLATE,
'L': L_TEMPLATE,
'I': I_TEMPLATE,
'O': O_TEMPLATE,
'T': T_TEMPLATE}
                      
# main screen initializes globla constants and shows start screen
def main():
	global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT
	pygame.init()
	#update the time every time the position of a piece changes
	FPSCLOCK = pygame.time.Clock()
	# initialize a window for display
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
	BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
	# set current window caption
	pygame.display.set_caption('MyTetris')
	showTextScreen('MyTetris')
	while True:
		pygame.mixer.music.load('ThemeA.mid')
		pygame.mixer.music.play(-1, 0.0)
		runGame()
		showTextScreen('Game Over!!!')
		pygame.mixer.music.stop()

def runGame():
	board = getBlankBoard()
	lastMoveDownTime = time.time()
	lastMoveSidewaysTime = time.time()
	lastFallTime = time.time()
	movingDown = False
	movingLeft = False
	movingRight = False
	score = 0
	level, fallFreq = calculateLevelAndFallFreq(score)

	fallingPiece = getNewPiece()
	nextPiece = getNewPiece()

	# while pieces are falling
	while True:
		# falling piece is None when current piece has landed/no piece in play
		if fallingPiece == None:

			#start shifting pieces
			fallingPiece = nextPiece
			nextPiece = getNewPiece()
			lastFallTime = time.time() #reset lastFallTime

			if not isValidPosition(board, fallingPiece):
				return

		checkForQuit()

		for event in pygame.event.get():

			# state of key is released
			if event.type == KEYUP:
				if (event.key == K_p):
					#Pause the game when P Key is pressed

					DISPLAYSURF.fill(BGCOLOR)
					pygame.mixer.music.stop()
					showTextScreen('Paused')
					pygame.mixer.music.play(-1, 0.0)
					lastFallTime = time.time()
					lastMoveDownTime = time.time()
					lastMoveSidewaysTime = time.time()

				# if the keys are lifted, then they are no longer moving in that direction
				elif (event.key == K_LEFT or event.key == K_a):
					movingLeft = False
				elif (event.key == K_RIGHT or event.key == K_d):
					movingRight = False
				elif (event.key == K_DOWN or event.key == K_s):
					movingDown = False

			# state of key is pressed
			elif event.type == KEYDOWN:
				if (event.key == K_LEFT or event.key == K_a) and isValidPosition(board, fallingPiece, adjX=-1):
						fallingPiece['x'] -= 1 # change the x coordinate
						movingLeft = True
						movingRight = False
						lastMoveSidewaysTime = time.time()

				elif (event.key == K_RIGHT or event.key == K_d) and isValidPosition(board, fallingPiece, adjX=1):
					fallingPiece['x'] += 1
					movingRight = True
					movingLeft = False
					lastMoveSidewaysTime = time.time()
				elif (event.key == K_UP or event.key == K_w):
					# get the next rotation in the template
					fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(SHAPES[fallingPiece['shape']])
					if not isValidPosition(board, fallingPiece):
						#switch back to old rotation if rotated position is not valid
						fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(SHAPES[fallingPiece['shape']])
				elif (event.key == K_q): #rotate the other direction
					fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(SHAPES[fallingPiece['shape']])
					if not isValidPosition(board, fallingPiece):
						fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(SHAPES[fallingPiece['shape']])
				elif (event.key == K_DOWN or event.key == K_s):
					movingDown = True
					if isValidPosition(board, fallingPiece, adjY=1):
						fallingPiece['y'] += 1
					lastMoveDownTime = time.time()
				elif event.key == K_SPACE:
					# all keys must be let go for a smooth shift downwards
					movingDown = False
					movingLeft = False
					movingRight = False

					# move down one box until position is no longer valid
					for i in range(1, NUMBOXHEIGHT):
						if not isValidPosition(board, fallingPiece, adjY=i):
							break
					# i - 1 because i is incremented before the break
					fallingPiece['y'] += i - 1


			#moving by holding Down the key
			# lastMoveSidewaysTime is set at the first keystroke, so if the key is held for a long
			# time, then the if statement will always be true, so change the position accordingly
		if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > MOVESIDEWAYSFREQ:
			if movingLeft and isValidPosition(board, fallingPiece, adjX=-1):
				fallingPiece['x'] -= 1
			elif movingRight and isValidPosition(board, fallingPiece, adjX=1):
				fallingPiece['x'] += 1
			lastMoveSidewaysTime = time.time()

		if movingDown and time.time() - lastMoveDownTime > MOVEDOWNFREQ and isValidPosition(board, fallingPiece, adjY=1):
			fallingPiece['y'] += 1
			lastMoveDownTime = time.time()


			#naturally falling piece
			# below is the condition for elapsed time
		if time.time() - lastFallTime > fallFreq:
			# has the piece landed?
			if not isValidPosition(board, fallingPiece, adjY=1):

				# add the piece to the board data structure
				addToBoard(board, fallingPiece)
				# erase completed lines from board data structure, pull boxes down, update score with number of lines removed
				score += removeCompleteLines(board)
				# depending on score, level and fall frequency will change
				level, fallFreq = calculateLevelAndFallFreq(score)
				fallingPiece = None # get a new piece
			else:
				#keep moving piece down
				fallingPiece['y'] += 1
				lastFallTime = time.time()

		#draw everything on the screen
		DISPLAYSURF.fill(BGCOLOR)
		drawBoard(board)
		drawStatus(score, level)
		drawNextPiece(nextPiece)
		if fallingPiece != None:
			drawPiece(fallingPiece)

		# updates the display as the game loops on the screen
		# tick makes the game run at a reasonable pace
		pygame.display.update()
		FPSCLOCK.tick(FPS)

# given text, font, color objects, calls render and returns Surface and Rect object for text
def makeTextObjects(text, font, color):
	surf = font.render(text, True, color)
	return surf, surf.get_rect()

# terminate function shared amongst most pygames
def terminate():
	pygame.quit()
	sys.exit()

# pygame uses an event queue
def checkForKeyPress():
	checkForQuit()

	for event in pygame.event.get([KEYDOWN, KEYUP]):
		if event.type == KEYDOWN:
			continue
		return event.key # we want KEYUP events
	return None # if no KEYUP events

# Function will show a GIANT white blob of text
# for key events like Game Startup / Game Over
def showTextScreen(text):
	# display large screen of text until a keystroke is detected
	titleSurf, titleRect = makeTextObjects(text, BIGFONT, TEXTSHADOWCOLOR)
	titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
	# draw one image onto another
	# Surface objects represent images
	# Rect objects represent rectangular areas

	DISPLAYSURF.blit(titleSurf, titleRect)

	#Draw the text
	titleSurf, titleRect = makeTextObjects(text, BIGFONT, TEXTCOLOR)
	titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
	DISPLAYSURF.blit(titleSurf, titleRect)

	#Draw additional press key to play text
	pressKeySurf, pressKeyRect = makeTextObjects('Press a key to play', BASICFONT, TEXTCOLOR)
	pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100 )
	DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

	# when user presses a key, display will stop
	# consistently loop and display screen as no keys are pressed
	while checkForKeyPress() == None:
		pygame.display.update()
		FPSCLOCK.tick

# if there is a quit event in the queue or user presses Esc, terminate
def checkForQuit():
	for event in pygame.event.get(QUIT):
		terminate()
	for event in pygame.event.get(KEYUP):
		if event.key == K_ESCAPE:
			terminate()
		pygame.event.post(event) # put the event back in the queue after you take it out

# every line completed is one point, every ten lines is up a level
def calculateLevelAndFallFreq(score):
	level = int(score / 10) + 1
	# fall freq starts at 0.27 and moves faster by 0.02 seconds each level
	# after level 14, the speed no longer changes (ln 277)
	fallFreq = 0.27 - level * 0.02 # change this equation to adjust difficulty per level
	return level, fallFreq

# piece data structure has shape, rotation index, x, y, color fields
def getNewPiece():
	# return a random piece of random rotation and color

	#random.choice selects a random element from nonempty sequence
	# pick OLIZST
	shape = random.choice(list(SHAPES.keys()))
	newPiece = {'shape': shape,
	# SHAPES[shape] is the array of rotations
	# rotation gives the index of the array
	'rotation': random.randint(0, len(SHAPES[shape]) - 1),
	'x' : int(NUMBOXWIDTH / 2) - int(TEMPLATEWIDTH / 2),
	'y': -2, # start the piece above the baord
	'color': random.randint(0, len(COLORS) - 1)}
	return newPiece

def addToBoard(board, piece):
	# nested for loops go through the entire grid of tetromino
	# if a box is an O, then that coordinate + the piece's coordinate is set on the board

	for x in range(TEMPLATEWIDTH):
		for y in range(TEMPLATEHEIGHT):
			if SHAPES[piece['shape']][piece['rotation']][y][x] != BLANK:
				# assumes the template is pivoted from the top left corner as the origin
				board[x + piece['x']][y + piece['y']] = piece['color']


# setting up a blank board column by column
def getBlankBoard():
	board = []
	for i in range(NUMBOXWIDTH):
		board.append([BLANK] * NUMBOXHEIGHT)
	return board

def isOnBoard(x, y):
	return x >= 0 and x < NUMBOXWIDTH and y < NUMBOXHEIGHT

def isValidPosition(board, piece, adjX=0, adjY=0):
	for x in range(TEMPLATEWIDTH):
		for y in range(TEMPLATEHEIGHT):
			isAboveBoard = y + piece['y'] + adjY < 0
			if isAboveBoard or SHAPES[piece['shape']][piece['rotation']][y][x] == BLANK:
				continue
				# disregard box if it is blank, or is above the board
			if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
				return False
				# return false if the piece is not on the baord
			if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
				return False
				# if the piece is NOT blank and the board piece is not blank... there is overlap... false
	return True


def isCompleteLine(board, y):
	for x in range(NUMBOXWIDTH):
		if board[x][y] == BLANK:
			return False
	return True

def removeCompleteLines(board):
	numLinesRemoved = 0
	y = NUMBOXHEIGHT - 1
	while y >= 0:
		if isCompleteLine(board, y):

			# start from the bottom row and work up
			for pullDownY in range(y, 0, -1):

				# copy values from row above to current row for all rows in range
				for x in range(NUMBOXWIDTH):
					board[x][pullDownY] = board[x][pullDownY - 1]
			for x in range(NUMBOXWIDTH):
				# make the top row blank
				board[x][0] = BLANK
			numLinesRemoved += 1
			# remember there is the case where the row you are copying
			# down is also complete, so you do not decrement y
		else:

			y -= 1
	return numLinesRemoved

# convert to pixel coordinates using box size in pixels * num of boxes
def convertToPixelCoords(boxx, boxy):
	return (XMARGIN + boxx * BOXSIZE, TOPMARGIN + boxy * BOXSIZE)

def drawBox(boxx, boxy, color, pixelx=None, pixely=None):
	if color == BLANK:
		return
	if pixelx == None and pixely == None:
		pixelx, pixely = convertToPixelCoords(boxx, boxy)
		# the left and top parameters are off by one to have a blank space between the boxes
	pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))

def drawBoard(board):
	# drawing the thick border around the board
	pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN - 3, TOPMARGIN - 7, (NUMBOXWIDTH * BOXSIZE) + 8, (NUMBOXHEIGHT * BOXSIZE) + 8), 5)

	# fill the background of the board
	pygame.draw.rect(DISPLAYSURF, BGCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE * NUMBOXWIDTH, BOXSIZE * NUMBOXHEIGHT))

	# draw the individual boxes
	for x in range(NUMBOXWIDTH):
		for y in range(NUMBOXHEIGHT):
			# drawBox already does NOT draw if the box is blank
			drawBox(x, y, board[x][y])

def drawStatus(score, level):
	# need a surface and rectangle
	scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
	scoreRect = scoreSurf.get_rect()

	# recall WINDOWWIDTH = 640
	scoreRect.topleft = (WINDOWWIDTH - 150, 20)
	DISPLAYSURF.blit(scoreSurf, scoreRect)

# for the NEXT piece, it is not drawn on the board
# must pass pixel parameters (where the next piece will be dispayed visally)
def drawPiece(piece, pixelx=None, pixely=None):
	# recall piece data structure specifies shape, rotation, and position
	# get the correct shape from the dictionary
	# and the corresponding orientation
	shapeToDraw = SHAPES[piece['shape']][piece['rotation']]
	if pixelx == None and pixely == None:
		# if pixels are not specified, use the position coords specified in the data strcture
		pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])
	
	# iterate through each box in the template
	# if the box is not blank, draw the box
	for x in range(TEMPLATEWIDTH):
		for y in range(TEMPLATEHEIGHT):
			if shapeToDraw[y][x] != BLANK:
				drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + y * BOXSIZE)

def drawNextPiece(piece):
	# draw the next text
	nextSurf = BASICFONT.render('NEXT:', True, TEXTCOLOR)
	nextRect = nextSurf.get_rect()
	nextRect.topleft = (WINDOWWIDTH - 120, 80)
	DISPLAYSURF.blit(nextSurf, nextRect)
	#draw the next piece at a fixed position on the screen
	drawPiece(piece, pixelx=WINDOWWIDTH-120, pixely=100)

# call the main function afater each function defitinion is executed
if __name__ == '__main__':
	main()
