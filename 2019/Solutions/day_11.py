import os
from collections import defaultdict
import numpy as np

from statemachine import StateMachine, operators

os.chdir(r"2019\Solutions")

with open(r"..\Inputs\day_11.txt") as file:
    program = [int(i) for i in file.read().split(",")]

arr = np.array([[0]*10]*5)

cardinals = [
    (0, 1),  # North or Up:     0
    (1, 0),  # East or Right:   1
    (0, -1),  # South or Down:  2
    (-1, 0)   # West or Left:   3
]


def turn(orientation, direction):
    return (orientation+direction) % 4


def move(x, y, orientation):
    i, j = cardinals[orientation]
    return x+i, y+j


robot = StateMachine(operators, program)


def paints(original_grid, start, orientation, robot):
    painter = robot.run(False)
    pos = start
    grid = original_grid.copy()
    while True:
        try:
            robot.send(grid[pos])
            grid[pos] = next(painter)
            direction = next(painter) or -1
            orientation = turn(orientation, direction)
            pos = move(*pos, orientation)
        except StopIteration:
            return grid


grid_1 = paints(defaultdict(lambda: 0), (0, 0), 0, robot)


def part_one():
    return len(grid_1)


robot.reset()

grid_2 = paints(defaultdict(lambda: 0, [((0, 0), 1)]), (0, 0), 0, robot)


def plot(grid):
    keys = grid.keys()
    x_max, x_min = max(x for x, y in keys), min(x for x, y in keys)
    y_max, y_min = max(y for x, y in keys), min(y for x, y in keys)
    x_length = abs(x_max - x_min)
    y_length = abs(y_max - y_min)
    x_length, y_length
    graph = np.array([[0] * (x_length+1)] * (y_length+1)).transpose()
    for x, y in keys:
        x_i, y_i = x-x_min, y-y_min
        graph[x_i, y_i] = grid[x, y]
    return graph


def draw(graph):
    return "\n".join(["".join(["." if i else " " for i in line]) for line in graph])


def part_two():
    return draw(plot(grid_2))


print(part_one())  # 2339
print(part_two())  # PGUEPLPR
