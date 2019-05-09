import random
from Entity import Entity
from status import Status

NUM_HUNTERS = 4


class Agent(Entity):
    """Class that represents agents in Treasure Keeper."""

    def __init__(self, pos, board):
        super().__init__(pos, board)
        self.pos = pos
        self.board = board
        self.direction = random.choice([0, 1, 2, 3])  # left, up, right, down
        self.chestLocations = []
        self.huntersStatus = [Status.ALIVE for _ in range(NUM_HUNTERS)]

    # AGENT DECISION

    def agentDecision(self):
        pass

    def isPlanSound(self):
        pass

    def deliberate(self):
        pass

    def reconsider(self):
        pass

    def execute(self):
        pass

    def impossibleIntention(self):
        pass

    def succeededIntention(self):
        pass
