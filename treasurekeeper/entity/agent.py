import random
import queue
from collections import deque

from .entity import Entity

from ..globals import HunterStatus
from ..position import Position

from ..search.strategy import DFS
from ..search.node import Node
from ..search.problem import Problem

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

    

    ###########
    # sensors #
    ###########

    def is_ahead(self, entity):
        """Checks if Entity entity is in the cell ahead of the agent."""
        ahead_pos = self.ahead_position()
        if not ahead_pos:
            return False
        else:
            return self.board.entity_in_pos(ahead_pos, entity)

    def ahead_position(self, other_dir=None):
        """Return position ahead of the agent depending on it's direction."""
        if other_dir is not None:
            dir_ = self.direction
        else:
            dir_ = other_dir

        if dir_ == "d":
            res = self.pos + Position(1, 0)
        elif dir_ == "l":
            res = self.pos + Position(0, -1)
        elif dir_ == "u":
            res = self.pos + Position(-1, 0)
        elif dir_ == "r":
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

    def look_fov(self, depth):
        """Look in a cone (FOV) in front of the agent."""
        seed = self.ahead_position()
        pos_fov = [seed]

        for d in range(depth):
            if self.direction == "d" or self.direction == "u":
                for i in range(-i, i + 1):
                    aux_pos = Position(seed.row + d, seed.col + i)
                    if self.board.position_is_valid(aux_pos):
                        pos_fov.append()
            elif self.direction == "l" or self.direction == "r":
                for i in range(-i, i + 1):
                    aux_pos = Position(seed.row + i, seed.col + d)
                    if self.board.position_is_valid(aux_pos):
                        pos_fov.append()
        return pos_fov

    #############
    # actuators #
    #############

    def rotate_left(self, agent_name):
        """Rotate the agent's facing direction to the left."""
        curr_dir_idx = DIRECTIONS.index(self.direction)
        if curr_dir_idx == 3:
            new_dir_idx = 0
        else:
            new_dir_idx = curr_dir_idx + 1
        self.dir = DIRECTIONS[new_dir_idx]
        sprite_fname = "_".join([agent_name, str(self.dir), ".png"])
        self.set_sprite(sprite_fname)

    def rotate_right(self, agent_name):
        """Rotate the agent's facing direction to the right."""
        curr_dir_idx = DIRECTIONS.index(self.direction)
        if curr_dir_idx == 0:
            new_dir_idx = 3
        else:
            new_dir_idx = curr_dir_idx - 1
        self.dir = DIRECTIONS[new_dir_idx]
        sprite_fname = "_".join([agent_name, str(self.dir), ".png"])
        self.set_sprite(sprite_fname)

    #######################
    #  search & planning  #
    #######################

    def buildPathPlan(pos):
        """Calculate sequence of actions to reach a certain position."""
        path = self.find_path(pos)
        actions = deque()

        for node in path:
            rotations = self.get_rotations(node.state)
            for action in rotations:
                actions.append(action)
            actions.append(self.actions["move_forward"])

        return actions

    def get_rotations(self, pos):
        """Calculate the sequence of rotations to face a certaion position."""
        actions = []
        ahead = self.ahead_position()
        action = self.rotate(pos)

        while action is not None:
            actions.append(action)
            next_dir = action.split("_")[1][0]  # hack
            action = self.rotate(pos, next_dir)
        return actions

    def rotate(self, pos, start_dir=None):
        """Decides which rotation to perform to face a certain position."""
        if pos not in self.board.adjacent_positions(self.pos):
            raise Exception("Can only decide rotation for adjacent positions.")
        else:
            ahead = self.ahead_position(start_dir)
            if ahead and pos == ahead:
                return None  # Maybe swap with no-action

            opposite = (pos.row == self.pos.row) != (pos.col == self.pos.col)
            if opposite:
                return random.choice([self.actions["rotate_left"],
                                     self.actions["rotate_right"]])
            else:
                if start_dir is not None:
                    dir_ = start_dir
                else:
                    dir_ = self.direction
                if dir_ == "d":
                    if pos.col < self.pos.col:
                        return self.actions["rotate_left"]
                    else:
                        return self.actions["rotate_right"]
                elif dir_ == "u":
                    if pos.col > self.pos.col:
                        return self.actions["rotate_left"]
                    else:
                        return self.actions["rotate_right"]
                elif dir_ == "l":
                    if pos.row < self.pos.row:
                        return self.actions["rotate_left"]
                    else:
                        return self.actions["rotate_right"]
                elif dir_ == "r":
                    if pos.row > self.pos.row:
                        return self.actions["rotate_left"]
                    else:
                        return self.actions["rotate_right"]

    def find_path(self, pos):
        """Find the path to a position in the board."""
        state0 = Node(self.pos, None)

        def equals(node1, node2):
            return node1.state.row == node2.row and \
                   node1.state.col == node2.col

        def is_goal(node):
            return equals(node, Node(pos))

        def operator(node):
            adjacent = self.board.adjacent_positions(node.state)
            return [Node(adj_pos, node) for adj_pos in adjacent]

        problem = Problem(state0, operator, is_goal, equals)

        return DFS(problem)
    

