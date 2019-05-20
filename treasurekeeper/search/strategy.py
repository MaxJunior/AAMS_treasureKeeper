import queue 

from queue import LifoQueue
from collections import deque

from .node import Node
from .problem import Problem


def DFS(problem):
    """Path search using DFS."""
    if not isinstance(problem, Problem):
        raise Exception("Not a Problem!")
    open_ = LifoQueue()
    visited = []

    curr = problem.state0
    done = False

    while not done:
        if problem.is_goal(curr):
            done = True
            break
        else:
            for node in problem.operator(curr):
                if not custom_in(node, visited, problem.equals):
                    open_.put(node)
            visited.append(curr)
            curr = open_.get()

    # build the path
    path = deque()
    path.append(curr)
    curr_build = curr
    while curr_build.parent is not None:
        path.appendleft(curr_build.parent)
        curr_build = curr_build.parent
    return list(path)


def BFS(problem):
    """Path search using BFS."""
    if not isinstance(problem, Problem):
        raise Exception("Not a Problem!")
    open_ = queue.Queue()
    visited = []

    curr = problem.state0
    done = False
    while not done:
        if problem.is_goal(curr):
            done = True
            break
        else:
            for node in problem.operator(curr):
                if not custom_in(node, visited, problem.equals):
                    open_.put(node)
            visited.append(curr)
            curr = open_.get()
    # build the path
    path = deque()
    path.append(curr)
    curr_build = curr
    while curr_build.parent is not None:
        path.appendleft(curr_build.parent)
        curr_build = curr_build.parent
    return list(path)


def custom_in(el, struct, comparator):
    """Custom in keyword, with a defined comparator."""
    for e in struct:
        if comparator(el, e):
            return True
    return False
