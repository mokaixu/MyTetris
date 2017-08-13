#Monica's Attemp at coding python

import random, time, pygame, sys 
from pygame.locals import *

# SETUP CONSTANTS
FPS = 25
WINDOWWIDTH = 640
WIDOWHEIGHT = 480
BOXSIZE = 20
NUMBOXWIDTH = 10
NUMBOXHEIGHT = 20
BLANK = '.'
MOVESIDEWAYSFREQ = 0.15 #when L/R keys are pressed, will move 0.15 boxes per second
MOVEDOWNFREQ = 0.1 #when down key is pressed, will move 0.1 boxes down per second
XMARGIN = int((WINDOWWIDTH - BOXSIZE * NUMBOXWIDTH) * 0.5) #space from window to canvas
TOPMARGIN = WINDOWHEIGHT - (BOXSIZE * NUMBOXHEIGHT) - 5 #board is drawn 5 pixels above window

# COLOR CONSTANTS
WHITE = (255, 255, 255)
GRAY = (185, 185, 185)
BLACK = (0, 0, 0)
RED = (155, 0, 0)
LIGHTRED = (175, 20, 20)
GREEN = (0, 155, 0)
LIGHTGREEN = (20, 175, 20)
BLUE = (0, 0, 155)
LIGHTBLUE = (20, 20, 175)
YELLOW = (155, 155, 0)
LIGHTYELLOW = (175, 175, 20)

BORDERCOLOR = BLUE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
COLORS = (BLUE, GREEN, RED, YELLOW)
LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW)
assert len(COLORS) == len(LIGHTCOLORS) #each color needs an associated light color for hue differentiation

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
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
	BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
	pygame.display.set_caption('Tetromino')

	showTextScreen('Tetromino')

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
			elif event.key == KEYDOWN:
					if (event.key == K_LEFT or event.key == K_a) and 
					#optional parameters adjx & adjy that act as shortcut (do not need to pass in object location, just the change)
					isValidPosition(board, fallingPiece, adjX=-1):
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

def showTextScreen(text):
	# display large screen of text until a keystroke is detected
	titleSurf, titleRect = makeTextObjects(text, BIGFONT, TEXTSHADOWCOLOR)
	titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
	# draw one image onto another
	# Surface objects represent images
	# Rect objects represent rectangular areas
	
	DISPLAYSURF.blit(titleSurf, titleRect)













