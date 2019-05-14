from typing import List
from tk_types import Pos, Content
from .status import HunterStatus
from .agent import Agent
from .jailcell import Jailcell

HUNTER_DESIRES = {"free": 0, "collect": 1, "flee": 2}
HUNTER_ACTIONS = {"free": 0, "collect": 1, "moveForward": 2, "rotateLeft": 3,
                  "rotateRight": 4}

expl_colors = ["blue", "green", "red", "yellow"]

class Hunter(Agent):

    def __init__(self, id, pos, board):
        """
         board : the game structure where the agents are competing
         position : hunter current position
         numberOfLock : number of time the agent have been locked by the keeper
         treasures : amount of treasure accumulated by the hunter
         huntersPositions : current positions of all the hunters in the game
         isAlive : True, is the hunter numberOfLock is <= 1,otherwise, False
        """
        sprite_fname = f"expl_{expl_colors[id]}"
        super().__init__(pos, board, sprite_fname, HUNTER_DESIRES, HUNTER_ACTIONS)
        self.id = id
        self.timesLocked = 0
        self.treasure = 0.0
        self.huntersPositions = []
        self.status = HunterStatus.ALIVE

    
    def free(self, jailcell):
        """Frees a locked hunter from Jailcell jailcell."""
        pass
    def updateHuntersPositions(self, huntersPos : List[Pos]):
        """set the current positions of the hunter in the board """
        self.huntersPositions = huntersPos

    def setStatus(self, status):
        """ checks if the hunter is alive, i.e. was locked 2 times by the hunter"""
        self.status = status

    def updateTimesLocked(self):
        """Updated when a hunter is locked by the keeper:
           case 0 : locked by the first time
           case 1 : second time is been locked , is this case the hunter is dead
           Otherwise : do nothing 
         """
        if self.timesLocked == 0:
            self.timesLocked = 1
        elif self.timesLocked == 1:
            self.timesLocked = 2
            self.setStatus(HunterStatus.DEAD)
        else:
            raise Exception(f"Invalid lock in hunter {self.id}.")

    """ TO FIXME  """
    def getAdjacentsPositions(self):
        """ This method will retrive all the valid adjacents positions of the hunter in 1 radius """
        pass

    def  keeperIsInAdjacentPositions(self) -> bool :
        """  method to check if keeper is in adjacentPositions """
        pass

    def move(self):
        """ method responsable for the hunter movement in the board"""
        pass
