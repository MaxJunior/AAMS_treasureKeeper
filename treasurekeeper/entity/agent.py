import random
import queue
from collections import deque

from .entity import Entity

from ..globals import HunterStatus
from ..position import Position

from ..search.strategy import DFS, BFS
from ..search.node import Node
from ..search.problem import Problem

NUM_HUNTERS = 4
DIRECTIONS = ["d", "l", "u", "r"]


class Agent(Entity):
    """Class that represents agents in Treasure Keeper."""

    def __init__(self, pos, board, sprite_fname, desires, actions, name):
        # left, up, right, down
        self.direction = random.choice(DIRECTIONS)
        sprite_fname = ".".join(["_".join([sprite_fname,
                                           str(self.direction)]),
                                "png"])

        super().__init__(pos, board, sprite_fname, name)

        self.pos = pos
        self.board = board
        self.chestLocations = []
        self.huntersStatus = [HunterStatus.ALIVE for _ in range(NUM_HUNTERS)]
        self.desires = desires
        self.actions = actions
        self.intention = None
        self.plan = deque()

    ###########
    # sensors #
    ###########

    def treasure_ahead(self, from_pos=None, other_dir=None):
        """Check if there's a treasure ahead."""
        ahead = self.ahead_position(from_pos, other_dir)
        return self.board.pos_occupied_treasure(ahead)

    def jailcell_ahead(self, from_pos=None, other_dir=None):
        """Check if there's a jailcell ahead."""
        ahead = self.ahead_position(from_pos, other_dir)
        return self.board.pos_occupied_jailcell(ahead)

    def hunter_ahead(self, from_pos=None, other_dir=None):
        """Check if there's a hunter ahead."""
        ahead = self.ahead_position(from_pos, other_dir)
        return self.board.pos_occupied_hunter(ahead)

    def is_ahead(self, entity, from_pos=None, other_dir=None):
        """Checks if Entity entity is in the cell ahead of the agent."""
        ahead_pos = self.ahead_position(from_pos, other_dir)
        if not ahead_pos:
            return False
        else:
            return self.board.entity_in_pos(ahead_pos, entity)

    def ahead_position(self, from_pos=None, other_dir=None):
        """Return position ahead of the agent depending on it's direction.
           from_pos -> if you want to specify another position
           other_dir -> if you want to specify another position
        """
        if other_dir is not None:
            dir_ = other_dir
        else:
            dir_ = self.direction

        if from_pos is not None:
            pos = from_pos
        else:
            pos = self.pos

        if dir_ == "d":
            res = pos + Position(1, 0)
        elif dir_ == "l":
            res = pos + Position(0, -1)
        elif dir_ == "u":
            res = pos + Position(-1, 0)
        else:  # dir_ == "r":
            res = pos + Position(0, 1)
        if not self.board.position_is_valid(res):
            return False
        else:
            return res

    def move_forward(self):
        """Move to position ahead of the agent."""
        ahead = self.ahead_position()
        print("move", ahead)
        if ahead:
            self.board.set_agent_position(self, ahead)
            return True
        else:
            return False

    def look_fov(self, depth, other_dir=None):
        """Look in a cone (FOV) in front of the agent."""
        seed = self.ahead_position()
        pos_fov = self.board.adjacent_positions(self.pos)
        if not seed:
            return pos_fov
        pos_fov.append(seed)

        if other_dir is not None:
            dir_ = other_dir
        else:
            dir_ = self.direction

        for d in range(1, depth):
            if dir_ == "d":
                for i in range(-d, d + 1):
                    aux_pos = Position(seed.row + d, seed.col + i)
                    if self.board.position_is_valid(aux_pos):
                        pos_fov.append(aux_pos)
            elif dir_ == "u":
                for i in range(-d, d + 1):
                    aux_pos = Position(seed.row - d, seed.col + i)
                    if self.board.position_is_valid(aux_pos):
                        pos_fov.append(aux_pos)
            elif dir_ == "l":
                for i in range(-d, d + 1):
                    aux_pos = Position(seed.row + i, seed.col - d)
                    if self.board.position_is_valid(aux_pos):
                        pos_fov.append(aux_pos)
            elif dir_ == "r":
                for i in range(-d, d + 1):
                    aux_pos = Position(seed.row + i, seed.col + d)
                    if self.board.position_is_valid(aux_pos):
                        pos_fov.append(aux_pos)

        return pos_fov

    #############
    # actuators #
    #############

    def rotate_left(self, agent_name):
        """Rotate the agent's facing direction to the left."""
        self.direction = self.calc_rotate("l", self.pos, self.direction)
        sprite_fname = ".".join(["_".join([agent_name, str(self.direction)]), "png"])
        self.set_sprite(sprite_fname)

    def rotate_right(self, agent_name):
        """Rotate the agent's facing direction to the right."""
        self.direction = self.calc_rotate("r", self.pos, self.direction)
        sprite_fname = ".".join(["_".join([agent_name, str(self.direction)]), "png"])
        self.set_sprite(sprite_fname)

    def calc_rotate(self, orientation, from_pos, from_dir):
        """Calculates the result of a rotation."""
        curr_dir_idx = DIRECTIONS.index(from_dir)
        if orientation == "l":
            if curr_dir_idx == 3:
                new_dir_idx = 0
            else:
                new_dir_idx = curr_dir_idx + 1
        elif orientation == "r":
            if curr_dir_idx == 0:
                new_dir_idx = 3
            else:
                new_dir_idx = curr_dir_idx - 1
        else:
            raise Exception("Invalid orientation.")

        return DIRECTIONS[new_dir_idx]

    #######################
    #  search & planning  #
    #######################

    def buildPathPlan(self, pos):
        """Calculate sequence of actions to reach a certain position."""
        path = self.find_path(pos)
        actions = deque()
        print("Goal ->", pos.row, pos.col)
        for node in path[1:]:
            pass  # print(node.state.row, node.state.col)

        aux_pos = self.pos
        aux_dir = self.direction
        for node in path[1:]:
            rotations = self.get_rotations(node.state, aux_pos, aux_dir)
            #print("Rotations to", node.state, "from", aux_pos, aux_dir)
            #print(rotations)
            for action in rotations:
                actions.append(action)
                o = "l" if action == 3 else "r"
                aux_dir = self.calc_rotate(o, aux_pos, aux_dir)
            actions.append(self.actions["move_forward"])
            aux_pos = node.state
        print(actions)
        return actions

    def get_rotations(self, pos, from_pos=None, other_dir=None):
        """Calculate the sequence of rotations to face a certain position."""

        actions = []

        if other_dir is not None:
            dir_ = other_dir
        else:
            dir_ = self.direction

        if from_pos is not None:
            from_pos = from_pos
        else:
            from_pos = self.pos
        #print("Get rotation from", from_pos, "to", pos)
        ahead = self.ahead_position(from_pos, dir_)
        action = self.rotate(pos, from_pos, dir_)
        aux_dir = dir_

        while action is not None:
            #print(action)
            actions.append(action)
            o = "l" if action == 3 else "r"
            aux_dir = self.calc_rotate(o, from_pos, aux_dir)
            action = self.rotate(pos, from_pos, aux_dir)
        return actions

    def rotate(self, pos, from_pos=None, other_dir=None):
        """Decides which rotation to perform to face a certain position."""
        #print("me", self.pos.row, self.pos.col)
        #print("rot", pos.row, pos.col)

        if other_dir is not None:
            dir_ = other_dir
        else:
            dir_ = self.direction

        if from_pos is not None:
            from_pos = from_pos
        else:
            from_pos = self.pos
        if pos not in self.board.adjacent_positions(from_pos):
            raise Exception("Can only decide rotation for adjacent positions.")
        else:
            ahead = self.ahead_position(from_pos, dir_)
            if ahead and pos == ahead:
                return None  # Maybe swap with no-action

            opposite = (pos.row == from_pos.row) != (pos.col == from_pos.col)
            if opposite:
                #print("Opposite")
                return random.choice([self.actions["rotate_left"],
                                     self.actions["rotate_right"]])
            else:
                if dir_ == "d":
                    if pos.col < from_pos.col:
                        return self.actions["rotate_left"]
                    else:
                        return self.actions["rotate_right"]
                elif dir_ == "u":
                    if pos.col > from_pos.col:
                        return self.actions["rotate_left"]
                    else:
                        return self.actions["rotate_right"]
                elif dir_ == "l":
                    if pos.row < from_pos.row:
                        return self.actions["rotate_left"]
                    else:
                        return self.actions["rotate_right"]
                elif dir_ == "r":
                    if pos.row > from_pos.row:
                        return self.actions["rotate_left"]
                    else:
                        return self.actions["rotate_right"]

    def find_path(self, pos):
        """Find the path to a position in the board."""
        state0 = Node(self.pos, None)

        def equals(node1, node2):
            return node1.state.row == node2.state.row and \
                   node1.state.col == node2.state.col

        def is_goal(node):
            return equals(node, Node(pos, None))

        def operator(node):
            adjacent = self.board.adjacent_positions(node.state)
            return [Node(adj_pos, node) for adj_pos in adjacent
                    if self.board.position_is_free(adj_pos)]

        problem = Problem(state0, operator, is_goal, equals)
        return BFS(problem)
