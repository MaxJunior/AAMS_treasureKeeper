"""
COURSE  : 
GROUP N : 48
76213   : Goncalo Lopes
79457   : Maxwell Junior
"""

from typing import List, Tuple

#________________________________________________________
# Types Annotations

Content = str
Pos = Tuple[int, int]
Board = List[List[Content]]
Group = List[Pos]
Move = List[Pos]
Adj =  List[Pos]

#________________________________________________________
# TAI content
def c_peg() -> Content:
    """ Returns the content of ocupied entry """
    return "O"
def is_peg (c: Content):
    """ Returns True if an entry is ocupied and False otherwise """
    return c == c_peg()

def c_empty ():
    """ Returns the content of empty entry """
    return "_"

def is_empty (c: Content):
    """ Returns True if an entry is false and False otherwise """
    return c == c_empty()

def c_blocked ():
    """ Returns the content of an blocked entry """
    return "X"

def is_blocked (c: Content):
    """ Returns True if an entry is blocked and False otherwise """
    return c == c_blocked()

def get_content(board : Board, pos : Pos) -> Content:
    """ Returns the content of the 'pos' entry of the 'board' """
    return board[pos[0]][pos[1]]

def set_content(board: Board, pos: Pos, content: Content) -> None :
    """ Sets the content of the 'pos' entry of the 'board' """
    board[pos[0]][pos[1]] = content
#_____________________________________________________________
# TAI pos

def make_pos (line: int, colune: int) -> Pos:
    """Creates a position."""
    return (line, colune)

def pos_l (pos: Pos) -> int:
    """Returns the line of the 'pos' position."""
    return pos[0]

def pos_c (pos: Pos) -> int:
    """Returns the column of the 'pos' position."""
    return pos[1]

def pos_is_valid(pos: Pos, board: Board) -> bool:
    """Returns True if 'pos' is inside the 'board' limits."""
    return 0 <= pos[0] < board_n_lines(board) and 0 <= pos[1] < board_n_columns(board)

def pos_sum(pos1: Pos, pos2: Pos) -> Pos:
    """Returns the sum of two positions."""
    return (pos1[0] + pos2[0], pos1[1] + pos2[1])


# _____________________________________________________________________________
# TAI Move

def make_move(p_initial: Pos, p_final: Pos) -> Move :
    """Create a move"""
    return [p_initial, p_final]

def move_initial (move: Move) -> Pos:
    """Returns the initial position"""
    return move[0]

def move_final(move: Move) -> Pos:
    """Returns the final position"""
    return move[1]
# _____________________________________________________________________________
# TAI Board


def board_n_lines(board: Board) -> int:
    """Returns the number of lines of the board"""
    return len(board)


def board_n_columns(board: Board) -> int:
    """Returns the number of columns of the board"""
    return len(board[0])

def print_board(board: Board) :
    """ prints the contents of the current board """
    lines = board_n_lines(board)
    columns = board_n_columns(board)

    for el in board :
        print(el)
        

def board_create_deep_copy(board: Board) -> Board:
    """Returns a deep copy of the board"""
    return [line[:] for line in board]


def find_empty_pos(board: Board) -> Group :
    """ Return an list of empty content in board """
    group = []

    for line in range(board_n_lines(board)):
        for column in range(board_n_columns(board)):
            curr_pos = make_pos(line, column)
            if(is_empty(get_content(board, curr_pos)) == True):
                group.append(curr_pos)
    return group



def board_moves(board : Board) -> List[Move]:
    """ find all valid moves in the board """

    """ all the adjecent (Nort, South, East, West) positions, each adjecent position
        have an inner and outer position. EX : "0,0,_" given the position (0,2), empty one,
        is South adjecent is : (0,1) the inner adj and (0,0) the outter adj;
    """
    # to fix : the radius of the range must/can be 2, i.e. two position in every direction
    # from the a position in the board  
    adjs = [ [(-1,0) , (-2,0)], [(1,0),(2,0)],[(0,-1),(0,-2)],[(0,1) , (0,2)]]

    def find_valid_move(board: Board, pos: Pos, adj: Adj) -> Move :
        "Giving an empty content and adj side find if is possible a valid move "

        adj_inner  = pos_sum(pos, adj[0])
        adj_outter = pos_sum(pos, adj[1])

        """ a move is valid if is inner and outter adjecent positions are valid and
            have 'O' as content
        """
        if ((pos_is_valid(adj_inner,board)  and is_peg(get_content(board,adj_inner))) and
            (pos_is_valid(adj_outter,board) and is_peg(get_content(board,adj_outter)))):
            return [adj_outter, pos]

    moves = []
    empty_positions = find_empty_pos(board)

    for empty_pos in empty_positions :
        for adj_pos in adjs:
            move = find_valid_move(board, empty_pos,adj_pos)
            if (move != None):
                moves.append(move)

    return moves

def  get_values_diff(val1: int, val2: int) -> int :

      if val1 - val2  == 0 :
          return 0
      return val1 - 1 if val1 > val2 else val1 + 1


def get_pos_intermediary(board: Board, pos1: Pos, pos2: Pos) -> Pos:

    """ Get the position between the inicial position and the final position  """

    pos1_line = pos_l(pos1)
    pos1_col  = pos_c(pos1)

    pos2_line = pos_l(pos2)
    pos2_col  = pos_c(pos2)

    """ The move its in the  """
    if get_values_diff(pos1_line, pos2_line) == 0 :
         return (pos1_line, get_values_diff(pos1_col, pos2_col))

    if get_values_diff(pos1_col, pos2_col) == 0:
        return (get_values_diff(pos1_line, pos2_line),pos1_col)



def board_perform_move(board: Board, move: Move) -> Board:

    def perform_move (board: Board, move: Move) -> Board :
        pos_init  = move[0]
        pos_final = move[1]

        """ Get the position between the inicial position and the final position  """
        pos_inter = get_pos_intermediary(board, pos_init, pos_final)

        """ Set the new board configuration by applying the move to the board """
        set_content(board, pos_init, c_empty())
        set_content(board, pos_inter, c_empty())
        set_content(board, pos_final, c_peg())

        return board

    """ Create a deep copy of the board """
    board_copy = board_create_deep_copy(board)

    """ Check if the move in part of valid moves, if true, perform the move,
        otherwise, return the board copy"""
    if move in board_moves(board):
        return perform_move(board_copy, move)

    else :
        return board_copy

def find_content_type_pos(board: Board, content: Content ) -> List[Move]:
    """ given a board an content type: return a list of positions 
       of the content type in the board """
    board_lines = board_n_lines(board)
    board_columns = board_n_columns(board)
    
    positions= []
    
    for line in range(board_lines):
        for column in range(board_columns):
            curr_pos = make_pos(line,column)
            if get_content(board, curr_pos) == content:
                positions.append(curr_pos)
    return positions

def board_content_type_amount(board: Board, content:Content)-> int:
    """ given a board and an content type : return the amount of content type in the
      board """
    amount = len(find_content_type_pos(board,content))
    
    return amount

def find_content_pos(board: Board, content: Content) -> List[Pos]:
    """ given a board and an content type :return the content of an a given type in the board

    """
    lines = range(0, board_n_lines(board))
    columns = range(0, board_n_columns(board))
    
    positions = [ (l,c) for l in lines for c in columns if get_content(board,make_pos(l,c)) == content]
    
    return positions
