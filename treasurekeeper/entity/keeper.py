from collections import deque 
import random
from .agent import Agent, DIRECTIONS
from .entity import Entity
from ..position import Position
from ..globals import EXPL_COLORS, HunterStatus

KEEPER_DESIRES = {"grab": 0, "lock": 1}
KEEPER_ACTIONS = {"grab": 0, "lock": 1, "move_forward": 2, "rotate_left": 3,
                  "rotate_right": 4}


class Keeper(Agent):
    def __init__(self, pos, board, chestLocations, jailcellLocations):
        """
         board          : the game structure where the agents are competing
         position       : keeper current position
         chestLocations : locations of the treasures
         cellLocations  : locations where keeper can detains an hunter

        """
        super().__init__(pos, board, "keeper", KEEPER_DESIRES, KEEPER_ACTIONS, "keeper")
        self.board = board
        self.pos = pos
        self.chestLocations = chestLocations
        self.jailcellLocations = jailcellLocations
        self.numberOfDeadHunters = 0
        self.carrying = None
        self.goal_jailcell = None
        self.walk_choice = 0

    def grab_hunter(self, hunter):
        """Grab a caught hunter."""
        if self.is_ahead(hunter):
            self.carrying = hunter
            # change sprite
            hunter_color = EXPL_COLORS[hunter.id]
            sprite_fname = f"keeper_expl_{hunter_color}_{self.direction}.png"
            self.set_sprite(sprite_fname)
            # update the hunter's status
            self.board.set_agent_position(hunter, self.pos, grab_flag=True)
            hunter.set_status(HunterStatus.GRABBED)
        else:
            raise Exception(f"Hunter {hunter.id} is not ahead of the keeper.")

    def lock_hunter(self, jailcell):
        """Lock the grabbed hunter."""
        if self.carrying is not None:
            if self.is_ahead(jailcell):
                # update jailcell
                jailcell.set_prisoner(self.carrying)
                # update hunter
                self.carrying.set_status(HunterStatus.LOCKED)
                self.carrying.update_times_locked()
                self.board.set_agent_position(self.carrying, jailcell.pos, True)
                # update keeper
                self.carrying = None
            else:
                raise Exception("Jailcell not ahead of the keeper.")
        else:
            raise Exception("Keeper isn't carrying a hunter.")

    def rotate_left(self):
        """Rotate keeper to the left."""
        name = "keeper"
        if self.carrying is not None:
            name = "_".join([name, f"expl_{self.carrying.get_color()}"])
        super().rotate_left(name)

    def rotate_right(self):
        """Rotate keeper to the right."""
        name = "keeper"
        if self.carrying is not None:
            name = "_".join([name, f"expl_{self.carrying.get_color()}"])
        super().rotate_right(name)

    def choose_jailcell(self):
        for pos in self.jailcellLocations:
            if not self.board.get_content(pos).is_occupied():
                return self.board.get_content(pos)

    def hunter_in_fov(self, depth, other_dir=None):
        """Check if there's a hunter in the hunter's fov."""
        fov = self.look_fov(depth, other_dir)
        for pos in fov:
            if self.board.pos_occupied_hunter(pos) and\
               self.board.get_content(pos).status != HunterStatus.LOCKED and\
               self.board.get_content(pos).status != HunterStatus.DEAD:
                return pos
        return False
    
    def get_adjacent_hunter_pos(self, hunter_pos):
        """Get a free pos adjacent to a hunter."""
        adj = self.board.adjacent_positions(hunter_pos)
        free = [a for a in adj if self.board.position_is_free(a)]
        if len(free) == 0:
            return None
        else:
            return random.choice(free)

    def move_forward(self):
        """Move to position ahead of the agent."""
        ahead = self.ahead_position()
        print("move", ahead)
        if ahead:
            self.board.set_agent_position(self, ahead)
            if self.carrying:
                self.board.set_agent_position(self.carrying, ahead, True)
            return True
        else:
            return False

    def random_rotate(self):
        """Rotate randomly."""
        return random.choice([KEEPER_ACTIONS["rotate_left"], KEEPER_ACTIONS["rotate_right"]])

    def execute(self):
        """Executes the next action according to a behavior."""
        #if len(self.plan) == 0:
        self.plan = deque()
        actions = self.reactive()
        if actions is None:
            return
        for a in actions:
            self.plan.append(a)

        action = self.plan.popleft()
        print("a", action)
        print("Action ->", action, list(self.actions.keys())[action[0]])

        if action[0] == KEEPER_ACTIONS["grab"]:
            self.grab_hunter(action[1])
        elif action[0] == KEEPER_ACTIONS["lock"]:
            self.lock_hunter(action[1])
        elif action[0] == KEEPER_ACTIONS["move_forward"]:
            self.move_forward()
        elif action[0] == KEEPER_ACTIONS["rotate_left"]:
            self.rotate_left()
        elif action[0] == KEEPER_ACTIONS["rotate_right"]:
            self.rotate_right()
        else:
            raise Exception("Invalid hunter action!")

    def reactive(self):
        res = []

        ahead = self.ahead_position()
        if not ahead:
            print("Facing the wall.")
            # facing the wall with no plan, rotate!
            res.append((self.random_rotate(), None))
            return res
        j_ahead = self.jailcell_ahead()
        if self.carrying and j_ahead and not j_ahead.is_occupied():
            print("Locking")
            self.goal_jailcell = None
            return [(KEEPER_ACTIONS["lock"], j_ahead)]
            
        elif self.carrying:
            if self.goal_jailcell is None:
                self.goal_jailcell = self.choose_jailcell()

            adj = self.board.adjacent_positions(self.pos)
            for a in adj:
                if self.goal_jailcell == self.board.get_content(a):
                    print("Carrying, jailcell adjacent.")
                    return [(rot, None) for rot in self.get_rotations(a)]

            print("Carrying, going for jailcell.")
            free = False
            while not free:
                random_pos = random.choice(self.board.adjacent_positions(self.goal_jailcell.pos))
                free = self.board.position_is_free(random_pos)
            print("j", random_pos)
            return [(action, None) for action
                    in self.buildPathPlan(random_pos)
                    if self.board]

        h_ahead = self.hunter_ahead()
        if h_ahead and\
           h_ahead.status != HunterStatus.LOCKED and\
           h_ahead.status != HunterStatus.DEAD:
            # grab hunter if treasure is ahead
            print("Grab!")
            res.append((KEEPER_ACTIONS["grab"], h_ahead))
            return res

        # check if hunter in adjacent positions
        adjacent = self.board.adjacent_positions(self.pos)
        for a in adjacent:
            if self.board.pos_occupied_hunter(a) and\
               self.board.get_content(a).status != HunterStatus.LOCKED and\
               self.board.get_content(a).status != HunterStatus.DEAD:
                print("hunter in adjacent, turn!")

                return [(rot, None) for rot in self.get_rotations(a)]

        # check if theres a hunter in fov
        h_in_fov_pos = self.hunter_in_fov(3)
        if h_in_fov_pos:
            pos = self.get_adjacent_hunter_pos(h_in_fov_pos)
            if pos is not None:
                print("Going for hunter")
                return [(action, None) for action
                        in self.buildPathPlan(pos)]

        # if there isn't, move randomly
        random_dir = random.choice(DIRECTIONS)
        ahead = self.ahead_position()
        if not ahead or not self.board.position_is_free(ahead) or self.walk_choice == 2:
            print("Random rotate.")
            action = self.random_rotate()
            self.walk_choice = 0
        else:
            print("Walk forward")
            action = KEEPER_ACTIONS["move_forward"]

        return [(action, None)]

        return res
