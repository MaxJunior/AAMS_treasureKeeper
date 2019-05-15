import random

from .agent import Agent
from .entity import Entity
from ..globals import EXPL_COLORS, HunterStatus, COLLECT_AMOUNTS

HUNTER_DESIRES = {"free": 0, "collect": 1, "flee": 2}
HUNTER_ACTIONS = {"free": 0, "collect": 1, "move_forward": 2, "rotate_left": 3,
                  "rotate_right": 4}


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
        sprite_fname = f"expl_{EXPL_COLORS[id]}"
        super().__init__(pos, board, sprite_fname, HUNTER_DESIRES,
                         HUNTER_ACTIONS)
        self.id = id
        self.timesLocked = 0
        self.gold = 0.0
        self.huntersPositions = []
        self.status = HunterStatus.ALIVE

    def free(self, jailcell):
        """Frees a locked hunter from Jailcell jailcell."""
        if self.is_ahead(jailcell) and (jailcell.prisoner is not None):
            jailcell.prisoner.escape(self, jailcell)
            aux = random.choice([-1, 1])
            # change the hunter's direction according to the new position so
            # it always looks to the freed hunter.
            if self.direction in ("u", "d"):
                if aux == -1:
                    self.direction = "r"
                else:
                    self.direction = "l"
                new_row = self.row
                new_col = self.col + aux
            elif self.direction in ("l", "r"):
                if aux == -1:
                    self.direction = "d"
                else:
                    self.direction = "u"
                new_row = self.row + aux
                new_col = self.col
            self.board.set_agent_position(self, new_row, new_col)
        else:
            raise Exception(f"Hunter {str(self.id)} can't \
                            free an empty Jailcell.")

    def escape(self, freer, jailcell):
        """Escape Jailcell jailcell, changing the position and status."""
        jailcell.release_prisoner()
        self.board.set_agent_position(self, freer.pos.row, freer.pos.col)

    def collect(self, treasure):
        """Collect gold from a treasure chest."""
        n_agents = self.board.agents_in_treasure(treasure)
        if 1 <= n_agents <= 4:
            amount = COLLECT_AMOUNTS[n_agents - 1]
        else:
            raise Exception(f"Invalid number of agents \
                            collecting: {n_agents}.")

        self.gold += treasure.remove_gold(amount)

    def updateHuntersPositions(self, huntersPos):
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

    def  keeperIsInAdjacentPositions(self):
        """  method to check if keeper is in adjacentPositions """
        pass

    def move_forward(self):
        """Move hunter to the position it is facing."""
        
        
