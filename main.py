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
J_SHAPE_TEMPLATE = [['.....',
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











