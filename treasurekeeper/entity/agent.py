import random
import queue

from .entity import Entity
from ..globals import HunterStatus
from ..position import Position

NUM_HUNTERS = 4
DIRECTIONS = ["d", "l", "u", "r"]


class Agent(Entity):
    """Class that represents agents in Treasure Keeper."""

    def __init__(self, pos, board, sprite_fname, desires, actions):
        # left, up, right, down
        self.direction = random.choice(DIRECTIONS)
        sprite_fname = ".".join(["_".join([sprite_fname,
                                           str(self.direction)]),
                                "png"])

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
        """Return position ahead of the agent depending on it's direction."""
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

    def move_forward(self):
        """Move to position ahead of the agent."""
        ahead = self.ahead_position()
        if ahead:
            self.board.set_agent_position(self, ahead)
            return True
        else:
            return False

    def rotate_left(self):
        """Rotate the agent's facing direction to the left."""
        curr_dir_idx = DIRECTIONS.index(self.direction)
        if curr_dir_idx == 3:
            new_dir_idx = 0
        else:
            new_dir_idx = curr_dir_idx + 1
        self.dir = DIRECTIONS[new_dir_idx]

    def rotate_right(self):
        """Rotate the agent's facing direction to the right."""
        curr_dir_idx = DIRECTIONS.index(self.direction)
        if curr_dir_idx == 0:
            new_dir_idx = 3
        else:
            new_dir_idx = curr_dir_idx - 1
        self.dir = DIRECTIONS[new_dir_idx]
