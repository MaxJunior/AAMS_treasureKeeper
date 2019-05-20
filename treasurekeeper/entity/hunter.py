import random
import itertools

from collections import deque

from .agent import Agent, DIRECTIONS
from .entity import Entity
from ..position import Position
from ..globals import EXPL_COLORS, HunterStatus, COLLECT_AMOUNTS, ChestStatus

HUNTER_DESIRES = {"free": 0, "collect": 1, "flee": 2}
HUNTER_ACTIONS = {"free": 0, "collect": 1, "move_forward": 2, "rotate_left": 3,
                  "rotate_right": 4}

HUNTER_ACTIONS_IDX = ["free", "collect", "move_forward", "rotate_left", "rotate_right"]


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
                         HUNTER_ACTIONS, sprite_fname)
        self.id = id
        self.times_locked = 0
        self.gold = 0.0
        self.hunter_positions = []
        self.status = HunterStatus.ALIVE
        self.danger = 0

    def updateHuntersPositions(self, huntersPos):
        """set the current positions of the hunter in the board """
        self.huntersPositions = huntersPos

    def set_status(self, status):
        """Set the hunter's status."""
        self.status = status

    def update_times_locked(self):
        """Update the times the hunter has been locked."""
        if self.timesLocked == 0:
            self.timesLocked = 1
        elif self.timesLocked == 1:
            self.timesLocked = 2
            self.set_status(HunterStatus.DEAD)
        else:
            raise Exception(f"Invalid lock on hunter {self.id}.")

    def get_color(self):
        """Get the hunter's color."""
        return EXPL_COLORS[self.id]

    def execute(self, behavior):
        """Executes the next action according to a behavior."""

        if behavior == "rGreedy":
            #if len(self.plan) == 0:
            self.plan = deque()
            actions = self.reactiveGreedy()
            if actions is None:
                return
            for a in actions:
                self.plan.append(a)

            action = self.plan.popleft()
        print("a", action)
        print("Action ->", action, list(self.actions.keys())[action[0]])

        if action[0] == HUNTER_ACTIONS["free"]:
            self.free(action[1])
        elif action[0] == HUNTER_ACTIONS["collect"]:
            self.collect(action[1])
        elif action[0] == HUNTER_ACTIONS["move_forward"]:
            self.move_forward()
        elif action[0] == HUNTER_ACTIONS["rotate_left"]:
            self.rotate_left()
        elif action[0] == HUNTER_ACTIONS["rotate_right"]:
            self.rotate_right()
        else:
            raise Exception("Invalid hunter action!")

    ###########
    # sensors #
    ###########

    def check_danger(self):
        """Check if keeper is in vicinity, updating danger."""
        for i in range(1, 4):
            aux_sums = [Position(row, col) for (row, col)
                        in list(itertools.product([-i, 0, i], repeat=2))
                        if (row, col) != (0, 0)]

            new_pos = [(self.pos + pos) for pos in aux_sums
                       if self.board.position_is_valid(self.pos + pos)]

            for pos in new_pos:
                if self.board.pos_occupied_keeper(pos):
                    self.danger = 4 - i
                    return

    def find_flee_pos(self):
        """Find a safe position to flee to."""
        fov = self.look_fov(3)
        # fov has farther positions at the end of the list
        return fov[-1]

    def treasure_in_fov(self, depth, other_dir=None):
        """Check if there's a treasure in the hunter's fov."""
        fov = self.look_fov(depth, other_dir)
        for pos in fov:
            if self.board.pos_occupied_treasure(pos) and\
               self.board.get_content(pos) != ChestStatus.EMPTY:
                return pos
        return False

    def get_adjacent_treasure_pos(self, treasure_pos):
        """Get a free pos adjacent to a treasure."""
        adj = self.board.adjacent_positions(treasure_pos)
        free = [a for a in adj if self.board.position_is_free(a)]
        if len(free) == 0:
            return None
        else:
            return random.choice(free)

    #############
    # actuators #
    #############

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
            raise Exception(f"Invalid number of agents collecting: {n_agents}.")

        self.gold += treasure.remove_gold(amount)

    def rotate_left(self):
        """Rotate hunter to the left."""
        name = f"expl_{self.get_color()}"
        super().rotate_left(name)

    def rotate_right(self):
        """Rotate hunter to the right."""
        name = f"expl_{self.get_color()}"
        super().rotate_right(name)

    def random_rotate(self):
        """Rotate randomly."""
        return random.choice([HUNTER_ACTIONS["rotate_left"], HUNTER_ACTIONS["rotate_right"]])

    ############
    # behavior #
    ############

    def reactiveGreedy(self):
        res = []

        if self.status != HunterStatus.ALIVE:
            # can't do anything here
            print("Hunter deaded.")
            return None
        else:
            ahead = self.ahead_position()
            if not ahead:
                print("Facing the wall.")
                # facing the wall with no plan, rotate!
                res.append((self.random_rotate(), None))
                return res

            self.check_danger()
            if self.danger == 2:
                print("Run away!")
                # run away! the keeper is near!
                flee_pos = self.find_flee_pos()
                print(flee_pos)
                return [(action, None) for action in
                        self.buildPathPlan(flee_pos)]

            t_ahead = self.treasure_ahead()
            #print("treasure_ahead ->", t_ahead)
            if t_ahead and t_ahead.status != ChestStatus.EMPTY:
                # collect treasure if treasure is ahead
                print("Collect!")
                res.append((HUNTER_ACTIONS["collect"], t_ahead))
                return res

            # check if treasure in adjacent fov
            adjacent = self.board.adjacent_positions(self.pos)
            for a in adjacent:
                if self.board.pos_occupied_treasure(a) and\
                   self.board.get_content(a).status != ChestStatus.EMPTY:
                    print("Treasure in fov, turn!")

                    return [(rot, None) for rot in self.get_rotations(a)]

            # check if theres a treasure in fov
            t_in_fov_pos = self.treasure_in_fov(3)
            if t_in_fov_pos:
                pos = self.get_adjacent_treasure_pos(t_in_fov_pos)
                if pos is not None:
                    print("Going for the treasure")
                    return [(action, None) for action
                            in self.buildPathPlan(pos)]

            # if there isn't, move randomly
            print("Going randomly")
            random_dir = random.choice(DIRECTIONS)

            free_pos = False
            while not free_pos:
                random_pos = random.choice(self.look_fov(3, random_dir))
                free_pos = self.board.position_is_free(random_pos)

            return [(action, None) for action in
                    self.buildPathPlan(random_pos)]

        return res
