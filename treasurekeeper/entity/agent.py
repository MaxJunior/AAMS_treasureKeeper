import random
import queue

from .entity import Entity
from ..globals import HunterStatus

NUM_HUNTERS = 4

class Agent(Entity):
    """Class that represents agents in Treasure Keeper."""

    def __init__(self, pos, board, sprite_fname, desires, actions):
        self.direction = random.choice(["d", "l", "u", "r"])  # left, up, right, down
        sprite_fname = ".".join(["_".join([sprite_fname, str(self.direction)]), "png"])

        super().__init__(pos, board, sprite_fname)

        self.pos = pos
        self.board = board
        self.chestLocations = []
        self.huntersStatus = [HunterStatus.ALIVE for _ in range(NUM_HUNTERS)]
        self.desires = desires
        self.actions = actions
        self.intention = None
        self.plan = queue.Queue()


    def is_ahead(self, entity):
        """Checks if Entity entity is in the cell ahead of the agent."""
        ahead_pos = self.ahead_position()
        if not ahead_pos:
            return False
        else:
            return self.board.entity_in_pos(ahead_pos, entity)

    def ahead_position(self):
        """Return position ahead of the agent depending on the direction it is facing."""
        if self.direction == "d":
            res = self.pos + Position(1, 0)
        elif self.direction == "l":
            res = self.pos + Position(0, -1)
        elif self.direction == "u":
            res = self.pos + Position(-1, 0)
        elif self.direction == "r":
            res = self.pos + Position(0, 1)

        if self.board.pos_is_valid(res):
            return False
        else:
            return res
        