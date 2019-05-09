from tk_types import Pos, Content
import position
from agent import Agent


class Keeper(Agent):
    def __init__(self, pos: Pos, board, contentType : Content, chestLocations, cellLocations):
        """ 
         board          : the game structure where the agents are competing
         position       : keeper current position
         chestLocations : locations of the treasures
         cellLocations  : locations where keeper can detains an hunter

        """
        self.board = board
        self.position = pos
        self.chestLocations = chestLocations
        self.numberOfDeadHunters = 0
        self.cellLocations = cellLocations
        self.carrying = False
