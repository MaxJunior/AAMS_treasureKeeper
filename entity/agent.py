import random
from .entity import Entity
from .status import HunterStatus
import queue

NUM_HUNTERS = 4


class Agent(Entity):
    """Class that represents agents in Treasure Keeper."""

    def __init__(self, pos, board, sprite_fname, desires, actions):
        super().__init__(pos, board, sprite_fname)
        self.pos = pos
        self.board = board
        self.direction = random.choice([0, 1, 2, 3])  # left, up, right, down
        self.chestLocations = []
        self.huntersStatus = [HunterStatus.ALIVE for _ in range(NUM_HUNTERS)]
        self.desires = desires
        self.actions = actions
        self.intention = None
        self.plan = queue.Queue()

    def setPosition(self, row :int, col :int):
        """ method to set the position of the Keeper, the position is setted if and only if
            is the new position is valid
            """
        newPos = Position.make_pos(row, col)
        if self.board.position_is_valid(newPos):
            self.pos = newPos

    def aheadPosition(self):
        if self.direction == 0:
            res = pos_sum(self.pos, make_pos(0, -1))
        elif self.direction == 1:
            res = pos_sum(self.pos, make_pos(-1, 0))
        elif self.direction == 2:
            res = pos_sum(self.pos, make_pos(0, 1))
        elif self.direction == 3:
            res = pos_sum(self.pos, make_pos(1, 0))
        