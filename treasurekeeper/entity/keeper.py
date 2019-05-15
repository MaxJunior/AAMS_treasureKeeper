from ..position import Position
from .agent import Agent
from .entity import Entity


class Keeper(Agent):
    def __init__(self, pos, board, chestLocations, cellLocations):
        """ 
         board          : the game structure where the agents are competing
         position       : keeper current position
         chestLocations : locations of the treasures
         cellLocations  : locations where keeper can detains an hunter

        """
        super().__init__(pos, board, "keeper", None, None)
        self.board = board
        self.position = pos
        self.chestLocations = chestLocations
        self.numberOfDeadHunters = 0
        self.cellLocations = cellLocations
        self.carrying = False
