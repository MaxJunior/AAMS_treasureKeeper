
from .agent import Agent
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
        super().__init__(pos, board, "keeper", KEEPER_DESIRES, KEEPER_ACTIONS)
        self.board = board
        self.pos = pos
        self.chestLocations = chestLocations
        self.jailcellLocations = jailcellLocations
        self.numberOfDeadHunters = 0
        self.carrying = None

    def grab_hunter(self, hunter):
        """Grab a caught hunter."""
        if self.is_ahead(hunter):
            self.carrying = hunter
            # change sprite
            hunter_color = EXPL_COLORS[hunter.id]
            sprite_fname = f"keeper_expl_{self.dir}_\
                             {hunter_color}_{self.dir}.png"
            self.set_sprite(sprite_fname)
            # update the hunter's status
            self.board.set_agent_position(hunter, self.pos)
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
                self.carrying.status.update_times_locked()
                self.board.set_agent_position(self.carrying, jailcell.pos)
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
            name = "_".join([name, f"_expl_{self.carrying.get_color()}"])
        super().rotate_left(name)

    def rotate_right(self):
        """Rotate keeper to the right."""
        name = "keeper"
        if self.carrying is not None:
            name = "_".join([name, f"_expl_{self.carrying.get_color()}"])
        super().rotate_right(name)
