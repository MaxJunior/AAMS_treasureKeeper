"""
COURSE  : AAMS
GROUP N : 48
76213   : Goncalo Lopes
79457   : Maxwell Junior
"""

from typing import List, Tuple
from tk_types import Content, Pos, Group, Move, Adj
from gui import GUI
from board import Board

N_CELLS = 12
# This sets the margin between each cell
MARGIN = 3

# Define some colors
BLACK = (30, 37, 48)
WHITE = (255, 255, 255)
GOLD = (216, 179, 78)

GAME_TITLE = "Treasure Keeper"

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = HEIGHT = 35

board = Board(None, None)
gui = GUI(N_CELLS, WIDTH, MARGIN, board)
gui.displayBoard()