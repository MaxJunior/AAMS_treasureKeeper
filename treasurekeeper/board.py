import pygame
import time

from .position import Position
from .globals import HunterStatus, STEP_TIME
from .entity.jailcell import Jailcell
from .entity.treasure import Treasure
from .entity.keeper import Keeper
from .entity.hunter import Hunter

JAIL_COORDS = [(1, 5), (5, 10), (10, 5), (5, 1)]
TREASURE_COORDS = [(2, 1), (10, 9), (2, 9), (10, 1), (6, 5)]
KEEPER_COORDS = (3, 2)
HUNTER_COORDS = [(7, 0), (10, 6), (1, 11), (0, 10)]


class Board:

    def __init__(self, width, gui=None):
        self.width = width
        self.board = [[0 for _ in range(width)] for _ in range(width)]
        self.gui = gui

        self.jailcells = [Jailcell(Position(pos[0], pos[1]), self)
                          for pos in JAIL_COORDS]
        self.treasures = [Treasure(Position(pos[0], pos[1]), self)
                          for pos in TREASURE_COORDS]
        self.keeper = Keeper(Position(KEEPER_COORDS[0], KEEPER_COORDS[1]),
                             self,
                             TREASURE_COORDS,
                             [Position(j[0], j[1]) for j in JAIL_COORDS])
        self.hunters = [Hunter(id, Position(pos[0], pos[1]), self)
                        for id, pos in enumerate(HUNTER_COORDS)]

        for jail in self.jailcells:
            self.board[jail.pos.row][jail.pos.col] = jail

        for treasure in self.treasures:
            self.board[treasure.pos.row][treasure.pos.col] = treasure

        for hunter in self.hunters:
            self.board[hunter.pos.row][hunter.pos.col] = hunter

        self.board[self.keeper.pos.row][self.keeper.pos.col] = self.keeper

    def get_content(self, pos):
        """ Returns the content of the 'pos' entry of the 'board' """
        return self.board[pos.row][pos.col]

    def set_content(self, pos, content):
        """Sets the content of the 'pos' entry of the 'board' """
        self.board[pos.row][pos.col] = content

    def board_width(self):
        """Get the board's width."""
        return self.width

    ############################
    # position-related methods #
    ############################

    def position_is_valid(self, pos):
        """Returns True if pos is inside the board's limits."""
        return 0 <= pos.row < self.width and \
            0 <= pos.col < self.width

    def position_is_free(self, pos):
        """Check if a board Position pos is occupied."""
        return self.board[pos.row][pos.col] == 0

    def entity_in_pos(self, pos, entity):
        """Check if Entity entity is in board Position pos."""
        row = pos.row
        col = pos.col
        return self.board[row][col] == entity

    def pos_occupied_hunter(self, pos):
        """Check if pos is occupied by a Hunter."""
        row = pos.row
        col = pos.col

        cell = self.board[row][col]
        if isinstance(cell, Hunter):
            return cell
        else:
            return False

    def pos_occupied_keeper(self, pos):
        """Check if pos is occupied by the Keeper."""
        row = pos.row
        col = pos.col

        cell = self.board[row][col]
        return cell == self.keeper

    def pos_occupied_treasure(self, pos):
        """Check if pos is occupied by a treasure."""
        row = pos.row
        col = pos.col

        cell = self.board[row][col]
        #print(pos, cell)
        if isinstance(cell, Treasure):
            return cell
        else:
            return False

    def pos_occupied_jailcell(self, pos):
        """Check if pos is occupied by a jailcell."""
        row = pos.row
        col = pos.col

        cell = self.board[row][col]
        if isinstance(cell, Jailcell):
            return cell
        else:
            return False

    def set_agent_position(self, agent, new_pos, grab_flag=False):
        """Set the position of an Agent agent."""

        if (self.position_is_valid(new_pos) and self.position_is_free(new_pos)) or grab_flag:
            self.board[agent.pos.row][agent.pos.col] = 0
            agent.pos = new_pos

            new_row = new_pos.row
            new_col = new_pos.col
            if not grab_flag:
                self.board[new_row][new_col] = agent
        else:
            raise Exception("Invalid position", new_pos)

    def adjacent_positions(self, pos):
        """Returns the adjacent positions (no diagonals)."""
        row = pos.row
        col = pos.col

        aux = (Position(1, 0), Position(0, 1),
               Position(-1, 0), Position(0, -1))
        adjacent = [pos + a_pos for a_pos in aux
                    if self.position_is_valid(pos + a_pos)]
        return adjacent

    def board_create_deep_copy(self):
        """Returns a deep copy of the board"""
        return [line[:] for line in self.board]

    def find_empty_pos(self):
        """ Return an list of empty content in board """
        group = []

        for line in range(self.board_n_lines()):
            for column in range(self.board_n_columns()):
                curr_pos = Position(line, column)
               # if(Content.is_empty(self.get_content(curr_pos))):
                #    group.append(curr_pos)
        return group

    def agents_in_treasure(self, treasure):
        """Get the number of agents collecting a Treasure."""
        adjacent = self.adjacent_positions(treasure.pos)

        count = 0
        for pos in adjacent:
            if self.pos_occupied_hunter(pos):
                count += 1
        print("agents_treasure", count)
        return count

    """ TO FIXME :  """
    def board_moves(self):
        """ find all valid moves in the board """

        """ all the adjecent (Nort, South, East, West) positions, each adjecent position
            have an inner and outer position. EX : "0,0,_" given the position (0,2), empty one,
            is South adjecent is : (0,1) the inner adj and (0,0) the outter adj;
        """
        # to fix : the radius of the range must/can be 2, i.e. two position in every direction
        # from the a position in the board  
        adjs = [[(-1, 0), (-2, 0)], [(1, 0), (2, 0)],
                [(0, -1), (0, -2)], [(0, 1), (0, 2)]]

        def find_valid_move(pos, adj):
            "Giving an empty content and adj side find if is possible a valid move "

            adj_inner = Pos.pos_sum(pos, adj[0])
            adj_outter = Pos.pos_sum(pos, adj[1])

            """ a move is valid if is inner and outter adjecent positions are valid and
                have 'O' as content
            """
            if ((Pos.pos_is_valid(adj_inner, self.board) and
                 Content.is_peg(self.get_content(adj_inner))) and
                (Pos.pos_is_valid(adj_outter, self.board) and
                 Content.is_peg(self.get_content(adj_outter)))):
                return [adj_outter, pos]

        moves = []
        empty_positions = self.find_empty_pos()

        for empty_pos in empty_positions:
            for adj_pos in adjs:
                move = self.find_valid_move(empty_pos, adj_pos)
                if (move is not None):
                    moves.append(move)

        return moves

    def get_values_diff(val1, val2):

        if val1 - val2 == 0:
            return 0
        return val1 - 1 if val1 > val2 else val1 + 1

    def get_pos_intermediary(self, pos1, pos2):

        """ Get the position between the inicial position and the final position  """

        pos1_line = Pos.pos_l(pos1)
        pos1_col = Pos.pos_c(pos1)

        pos2_line = Pos.pos_l(pos2)
        pos2_col = Pos.pos_c(pos2)

        """ The move its in the  """
        if self.get_values_diff(pos1_line, pos2_line) == 0:
            return (pos1_line, self.get_values_diff(pos1_col, pos2_col))

        if self.get_values_diff(pos1_col, pos2_col) == 0:
            return (self.get_values_diff(pos1_line, pos2_line), pos1_col)

    def board_perform_move(self, move):
        pass

    def perform_move(self, move):
        pos_init = move[0]
        pos_final = move[1]

        """ Get the position between the inicial position and the final position  """
        pos_inter = self.get_pos_intermediary(pos_init, pos_final)

        """ Set the new board configuration by applying the move to the board """
        self.set_content(pos_init, Content.c_empty())
        self.set_content(pos_inter, Content.c_empty())
        self.set_content(pos_final, Content.c_peg())

        return self.board

        """ Create a deep copy of the board """
        board_copy = self.board_create_deep_copy()

        """ Check if the move in part of valid moves, if true, perform the move,
            otherwise, return the board copy"""
        if move in self.board_moves():
            return perform_move(board_copy, move)

        else:
            return board_copy

    def find_content_type_pos(self, content):
        """ given a board an content type: return a list of positions 
        of the content type in the board """
        board_lines = self.board_n_lines()
        board_columns = self.board_n_columns()
        
        positions = []
        
        for line in range(board_lines):
            for column in range(board_columns):
                curr_pos = Pos.make_pos(line, column)
                if self.get_content(curr_pos) == content:
                    positions.append(curr_pos)
        return positions

    def board_content_type_amount(self, content):
        """ given a board and an content type : return the amount of content type in the
        board """
        amount = len(self.find_content_type_pos(content))

        return amount

    def find_content_pos(self, content):
        """ given a board and an content type :return the content of an a given type in the board

        """
        lines = range(0, self.board_n_lines())
        columns = range(0, self.board_n_columns())

        positions = [(l, c) for l in lines for c in columns
                     if self.get_content(Pos.make_pos(l, c)) == content]

        return positions

    def run(self):
        done = False
        while(not done):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                #elif event.type == pygame.KEYDOWN:
            self.gui.displayBoard()
            self.step()
            self.displayEntities()
            time.sleep(STEP_TIME)

    def displayEntities(self):
        for entity in self.hunters:
            self.gui.draw_fov(entity)
        for entity in self.hunters:
            if entity.status == HunterStatus.ALIVE:
                self.gui.displayEntity(entity)

        for entity in self.treasures:
            self.gui.displayEntity(entity)
        for entity in self.jailcells:
            self.gui.displayEntity(entity)
        self.gui.displayEntity(self.keeper)

    def removeEntities(self):
        for entity in self.hunters:
            self.gui.removeEntity(entity)
        for entity in self.treasures:
            self.gui.removeEntity(entity)
        for entity in self.jailcells:
            self.gui.removeEntity(entity)
        
        self.gui.removeEntity(self.keeper)

    def step(self):
        print("############### KEEPER ################")
        self.keeper.execute()
        for hunter in self.hunters:
            print("################", hunter.name, "################")
            hunter.execute("rGreedy")
        

    def stop(self):
        pass

    def associateGUI(self, gui):
        self.gui = gui
