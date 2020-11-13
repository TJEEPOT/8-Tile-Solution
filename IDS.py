#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Solution of the 8-Tile problem.

Module  : CMP-6040A0 - Artificial Intelligence, Assignment 1
File    : IDS.py
Date    : Tuesday 13 October 2020
Desc.   : An algorithm which solves the (3 x 3) 8-Tile problem by utilising Iterative Deepening Depth First Search.
History : 13/10/2020 - v1.0 - Create project file.
          04/11/2020 - v1.1 - Placeholder functions defined
          13/11/2019 - v1.2 - Algorithm working but with too many calls reported. Unable to track down issue.
"""
import copy
import time

__author__ = "Martin Siddons"


"""
Results:
Instance 1:
16 moves, 85994 calls in 1.020 seconds

etc
"""


def is_goal(grid):
    """Check if the solution state has been found.

    To be considered complete, all tiles must be in numerical order with the blank tile (0) in the bottom right
    corner of the grid. This code works no matter the size of the grid used.

    :param grid: Current state of the puzzle grid
    :return:     Boolean, true if the solution has been found.
    """
    n = len(grid)  # find the length of one side of the grid
    prev_tile = 0
    for row in grid:
        for tile in row:
            if tile != prev_tile + 1:  # Check if tiles are in order. The last tile fails this check as it is '0'
                if prev_tile != n * n - 1:  # If the previous tile is not the second-from-last, the puzzle isn't solved
                    return False
            prev_tile += 1
    return True


def move_blank(i, j, n):
    """Generator to change the position of the blank tile.

    The movement of the blank tile is dependant on which tiles surround it.

    :param i: The row of the blank tile.
    :param j: The column of the blank tile.
    :param n: The square root of the puzzle area (i.e. for a 4x4 puzzle, n = 4)
    :return:  The row and column of the tile to switch the blank with.
    """
    if i + 1 < n:   # check for a tile to the bottom
        yield (i + 1, j)
    if i - 1 >= 0:  # check for a tile to the top
        yield (i - 1, j)
    if j + 1 < n:   # check for a tile to the right
        yield (i, j + 1)
    if j - 1 >= 0:  # check for a tile to the left
        yield (i, j - 1)


def move(state):
    """Find the next state to move to based on the current state

    :param state: Array containing the current location of the blank tile and a list of lists of the current position
    of all tiles.
    :return:      The next state of the puzzle, where the blank tile has moved once.
    """
    [i, j, grid] = state
    n = len(grid)
    for pos in move_blank(i, j, n):
        i1, j1 = pos  # assign the new blank tile position
        grid[i][j], grid[i1][j1] = grid[i1][j1], grid[i][j]  # swap the blank tile to the new position
        yield [i1, j1, grid]
        grid[i][j], grid[i1][j1] = grid[i1][j1], grid[i][j]  # reset state for next blank movement


def dls_rec(path, limit):
    """Depth Limited Search called recursively to a given depth.

    :param path:  List of all states from the initial state to the current state
    :param limit: Depth to iterate down to
    :return:      List containing the number of moves from start state to finish state, the total number of calls
    made to move() and a flag for if there are any remaining nodes.
    """
    total_calls = 0

    if limit == 0:
        if is_goal(path[-1][2]):  # pass the grid of the last state in the path
            moves = len(path) - 1  # don't count the initial state as a move
            return [moves, total_calls, False]
        else:
            return [None, total_calls, True]  # we didn't find a solution yet but there are child nodes to discover
    else:
        cutoff = False  # this is true if there are child nodes but we can't reach them at the current depth
        last_state = copy.deepcopy(path[-1])
        for nextState in move(last_state):
            total_calls += 1
            if nextState not in path:
                next_path = path + [nextState]
                moves, calls, remaining_moves = dls_rec(next_path, limit - 1)
                total_calls += calls

                if moves is not None:
                    return [moves, total_calls, False]  # unwinding recursion as solution was found
                if remaining_moves:
                    cutoff = True  # solution not found but there are child nodes, increase limit

        return [None, total_calls, cutoff]  # we didn't find a solution here, report if there are child nodes left


def iddfs_rec(path):
    """Depth First Search of given state with Iterative Deepening.

    Sets up iterative deepening on the depth limited search algorithm to discover the shortest path to the solution
    without exceeding the size of the recursive stack.

    :param path: Initial state of puzzle to solve.
    :return:     List containing the number of moves taken to solve and the total number of calls made to the move
    procedure.
    """
    total_calls = 0
    limit = 0

    while True:
        moves, calls, remaining_moves = dls_rec(path, limit)
        total_calls += calls

        if moves is not None:
            return [moves, total_calls]
        elif not remaining_moves:
            return None
        limit += 1


def main():
    """Main function.

    Builds a list of starting states with the state representation [i, j, [[1, 2, 3], [4, 5, 6], [7, 8, 0]]] where 'i'
    and 'j' are the coordinates of the empty space and the following lists show the positions of the 8 tiles from
    left to right, top to bottom, with 0 representing the empty space. These states are then passed into the IDS
    algorithm to be processed.
    """
    states_list = [
                    (0, 0, [[0, 7, 1], [4, 3, 2], [8, 6, 5]]),
                    (0, 2, [[5, 6, 0], [1, 3, 8], [4, 7, 2]]),
                    (1, 0, [[1, 2, 3], [0, 5, 6], [4, 7, 8]])
                    ]

    for i, state in enumerate(states_list):
        print("Instance {}:".format(i + 1), end=' ')
        start_time = time.perf_counter()
        solution = iddfs_rec([state])
        end_time = time.perf_counter()
        total_time = end_time - start_time

        if solution is None:
            print("No Solution")
        else:
            print("{} moves, {} calls in {:0.3f} seconds".format(
                solution[0], solution[1], total_time))


main()
