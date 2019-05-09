import position
from tk_types import Board_Type, Content, Move, Adj, Pos


class Board:

    def __init__(self, listPos: Board_Type):
        self.board = listPos

    def get_content(self, pos: Position) -> Content:
        """ Returns the content of the 'pos' entry of the 'board' """
        return self.board[pos[0]][pos[1]]

    def board_n_lines(self) -> int:
        """Returns the number of lines of the board"""
        return len(self.board)

    def set_content(self, pos: Position, content: Content) -> None:
        """ Sets the content of the 'pos' entry of the 'board' """
        self.board[pos[0]][pos[1]] = content

    def board_n_columns(self) -> int:
        """Returns the number of columns of the board"""
        return len(self.board[0])

    def pos_is_valid(self, pos: Position) -> bool:
        """Returns True if 'pos' is inside the 'board' limits."""
        return 0 <= pos[0] < self.board_n_lines() and \
            0 <= pos[1] < self.board_n_columns()

    def print_board(self):
        """ prints the contents of the current board """

        for el in self.board:
            print(el)

    def board_create_deep_copy(self):
        """Returns a deep copy of the board"""
        return [line[:] for line in self.board]

    def find_empty_pos(self):
        """ Return an list of empty content in board """
        group = []

        for line in range(self.board_n_lines()):
            for column in range(self.board_n_columns()):
                curr_pos = Position.make_pos(line, column)
                if(Content.is_empty(self.get_content(curr_pos))):
                    group.append(curr_pos)
        return group

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

        def find_valid_move(pos: Pos, adj: Adj) -> Move :
            "Giving an empty content and adj side find if is possible a valid move "

            adj_inner = Position.pos_sum(pos, adj[0])
            adj_outter = Position.pos_sum(pos, adj[1])

            """ a move is valid if is inner and outter adjecent positions are valid and
                have 'O' as content
            """
            if ((Position.pos_is_valid(adj_inner, self.board) and
                 Content.is_peg(self.get_content(adj_inner))) and
                (Position.pos_is_valid(adj_outter, self.board) and
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

    def get_values_diff(val1: int, val2: int) -> int :

        if val1 - val2 == 0:
            return 0
        return val1 - 1 if val1 > val2 else val1 + 1

    def get_pos_intermediary(self, pos1: Pos, pos2: Pos) -> Pos:

        """ Get the position between the inicial position and the final position  """

        pos1_line = Position.pos_l(pos1)
        pos1_col = Position.pos_c(pos1)

        pos2_line = Position.pos_l(pos2)
        pos2_col = Position.pos_c(pos2)

        """ The move its in the  """
        if self.get_values_diff(pos1_line, pos2_line) == 0:
            return (pos1_line, self.get_values_diff(pos1_col, pos2_col))

        if self.get_values_diff(pos1_col, pos2_col) == 0:
            return (self.get_values_diff(pos1_line, pos2_line), pos1_col)


def board_perform_move(self, move: Move) -> Board:

    def perform_move(self, move: Move) -> Board:
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

    def find_content_type_pos(self, content: Content):
        """ given a board an content type: return a list of positions 
        of the content type in the board """
        board_lines = self.board_n_lines()
        board_columns = self.board_n_columns()
        
        positions = []
        
        for line in range(board_lines):
            for column in range(board_columns):
                curr_pos = Position.make_pos(line, column)
                if self.get_content(curr_pos) == content:
                    positions.append(curr_pos)
        return positions

    def board_content_type_amount(self, content: Content)-> int:
        """ given a board and an content type : return the amount of content type in the
        board """
        amount = len(self.find_content_type_pos(content))

        return amount

    def find_content_pos(self, content: Content):
        """ given a board and an content type :return the content of an a given type in the board

        """
        lines = range(0, self.board_n_lines())
        columns = range(0, self.board_n_columns())

        positions = [(l, c) for l in lines for c in columns
                     if self.get_content(Position.make_pos(l, c)) == content]

        return positions
