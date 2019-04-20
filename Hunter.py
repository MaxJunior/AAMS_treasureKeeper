

from typing import List
from TK_Types import Pos,Content

class Hunter :
    def __init__(self,pos: Pos, board, contentType : Content):
        """ 
         board : the game structure where the agents are competing
         position : hunter current position
         numberOfLock : number of time the agent have been locked by the keeper
         treasures : amount of treasure accumulated by the hunter
         huntersPositions : current positions of all the hunters in the game
         isAlive : True, is the hunter numberOfLock is <= 1,otherwise, False
        """
        self.board = board
        self.position = pos
        self.numberOfLock = 0
        self.treasures = 0.0
        self.huntersPositions = []
        self.isAlive = True
    

    def updateHuntersPositions(self, huntersPos : List[Pos]):
        """set the current positions of the hunter in the board """
        self.huntersPositions = huntersPos
    
    def setIsAlive(self, boolVal :bool ):
        """ checks if the hunter is alive, i.e. was locked 2 times by the hunter"""
        self.isAlive = boolVal
    
    def updateNumberOfLock (self):
        """updated when the hunter is locked by the hunter :
           case 0 : locked by the first time
           case 1 : second time is been locked , is this case the hunter is dead
           Otherwhise : do nothing 
         """
        if self.numberOfLock == 0 :
            self.numberOfLock += 1
        elif self.numberOfLock == 1 :
            self.numberOfLock +=1
            self.setIsAlive(False)
                    
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