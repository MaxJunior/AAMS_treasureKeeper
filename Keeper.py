from TK_Types import Pos,Content
import Position

class Keeper :
    def __init__(self,pos: Pos, board, contentType : Content, chestLocations,cellLocations ):
        """ 
         board          : the game structure where the agents are competing
         position       : keeper current position
         chestLocations : locations of the treasures
         cellLocations  : locations where keeper can detains an hunter

        """
        self.board = board
        self.position = pos
        self.chestLocations = chestLocations
        self.numberOfDeathHunters = 0
        self.cellLocations = cellLocations
        


        def setPosition(row :int,col :int):
            """ method to set the position of the Keeper, the position is setted if and only if
                is the new position is valid
             """
            newPos = Position.make_pos(row,col)
            if self.board.position_is_valid(newPos):
                self.position = newPos    

