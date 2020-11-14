#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Solution of the 8-Tile problem.

Module  : CMP-6040A0 - Artificial Intelligence, Assignment 1
File    : IDS.py
Date    : Tuesday 13 October 2020
Desc.   : An algorithm which solves the (3 x 3) 8-Tile problem by utilising an Iterative Deepening A* approach.
History : 13/10/2020 - v1.0 - Create project file.
          13/11/2020 - v1.1 - Create placeholder functions and finish estimate_distance
"""
import copy
import sys
import time

__author__ = "Martin Siddons"

"""
Results:
Instance 1:
16 moves, 263 calls in 1.000 seconds

etc
"""


def is_goal(state):
    """Check if the solution state has been found.

    All tiles must be in numerical order with the blank tile (0) in the bottom right corner of the grid. This code
    works no matter the size of the grid used.

    :param state: Current state of the puzzle
    :return:      Boolean, true if the solution has been found.
    """
    grid = state[2]
    n = len(grid)  # find the length of one side of the grid
    prev_tile = 0

    for row in grid:
        for tile in row:
            if tile != prev_tile + 1:  # Check if tiles are in order. The last tile fails this check as it is '0'
                if prev_tile != n * n - 1:  # If the previous tile is not the second-from-last, the puzzle isn't solved
                    return False
            prev_tile += 1
    return True


def estimate_distance(state):
    """Find the distance of all tiles on the grid to their expected positions

    This finds the sum of the manhattan distances of all tiles from the current state to the goal state. The
    algorithm works no matter the size of the grid used.

    :param state: Current state of the puzzle.
    :return:      Int, sum of manhattan distances for all tiles on the grid.
    """
    grid = state[2]
    n = len(grid)  # find the length of one side of the grid
    distance = 0

    for i in range(n):
        for j in range(n):
            cur_tile = grid[i][j]
            if cur_tile == 0:
                continue  # skip the empty tile as its distance is inconsequential
            else:
                goal_i = int((cur_tile - 1) / n)  # the row number of the target destination
                goal_j = (cur_tile - 1) % n       # the column number of the target destination
                distance_i = abs(i - goal_i)      # the absolute vertical distance from current tile to the target
                distance_j = abs(j - goal_j)      # the absolute horizontal distance from current tile to the target
                distance += distance_i + distance_j

    return distance


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


def search(path, cost, bound):
    """Find the best game state to expand to from the current state.

    Uses A* to check all child nodes from the current path and return the smallest value where the value is the sum
    of the distance travelled so far and the estimated distance to the goal.
    
    :param path:  The list of nodes travelled from the root to the current node.
    :param cost:  The distance travelled to this node (the number of moves to get to this point).
    :param bound: The estimation of the distance from this node to the goal.
    :return:      An array of the lowest f-value found (or 0 if found, or None if not found) and the number of calls.
    """
    total_calls = 0
    last_state = copy.deepcopy(path[-1])
    total_distance = cost + estimate_distance(last_state)

    if total_distance > bound:
        return [total_distance, 0, total_calls]  # since the total distance is too large, update the f_min.
    if is_goal(last_state):
        moves = len(path) - 1  # don't count the initial state as a move
        return [0, moves, total_calls]  # '0' sent for f_min to indicate goal has been found

    f_min = sys.maxsize  # variable for the smallest f-value
    for nextState in move(last_state):
        total_calls += 1
        if nextState not in path:
            next_path = path + [nextState]
            result, moves, calls = search(next_path, cost + 1, bound)
            total_calls += calls

            if result == 0:
                return [0, moves, total_calls]  # unwinding recursion as solution was found
            if result < f_min:
                f_min = result  # solution not found but the distance is closer, update it

    return [f_min, None, total_calls]


def ida_star(state):
    """Performs Iterative Deepening on an A* search from root state to goal state.

    Discovers the shortest path to the solution without exceeding the size of the recursive stack.

    :param state: List containing the initial state of puzzle to solve.
    :return:      List containing the number of moves taken to solve and the total number of calls made to the move
    procedure.
    """

    bound = estimate_distance(state)  # initial depth to expand to is equal to the minimum distance to find the goal
    total_calls = 0
    path = [state]

    while True:
        f_min, moves, calls = search(path, 0, bound)
        total_calls += calls

        if f_min == 0:  # path found
            return [moves, total_calls]
        if f_min is sys.maxsize:  # no path found
            return None

        bound = f_min  # increase the depth to be equal to the closest node to the goal


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
                    (2, 0, [[3, 5, 6], [1, 2, 7], [0, 8, 4]]),
                    (1, 1, [[7, 3, 5], [4, 0, 2], [8, 1, 6]]),
                    (2, 0, [[6, 4, 8], [7, 1, 3], [0, 2, 5]]),
                    (0, 2, [[3, 2, 0], [6, 1, 8], [4, 7, 5]]),
                    (0, 0, [[0, 1, 8], [3, 6, 7], [5, 4, 2]]),
                    (2, 0, [[6, 4, 1], [7, 3, 2], [0, 5, 8]]),
                    (0, 0, [[0, 7, 1], [5, 4, 8], [6, 2, 3]]),
                    (0, 2, [[5, 4, 0], [2, 3, 1], [8, 7, 6]]),
                    (2, 1, [[8, 6, 7], [2, 5, 4], [3, 0, 1]]),
                    (1, 0, [[1, 2, 3], [0, 5, 6], [4, 7, 8]])
                    ]

    for i, state in enumerate(states_list):
        print("Instance {}:".format(i + 1), end=' ')
        start_time = time.perf_counter()
        solution = ida_star(state)
        end_time = time.perf_counter()
        total_time = end_time - start_time

        if solution is None:
            print("No Solution")
        else:
            print("{} moves, {} calls in {:0.3f} seconds".format(
                solution[0], solution[1], total_time))

# estimate_distance test
# print(estimate_distance([[0, 7, 1], [4, 3, 2], [8, 6, 5]]))  # should give '14'

main()
