
from TK_Types import Content

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