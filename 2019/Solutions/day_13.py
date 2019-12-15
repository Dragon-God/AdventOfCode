import os
from collections import Counter

from statemachine import StateMachine, operators
from doubledict import DoubleDict

os.chdir(r"2019\Solutions")

with open(r"..\Inputs\day_13.txt") as file:
    program = [int(i) for i in file.read().split(",")]

elements = [
    "empty",
    "wall",
    "block",
    "paddle",
    "ball"
]
arcade = StateMachine(operators, program)
play_arcade = StateMachine(operators, [2]+program[1:])


def initialise(machine):
    machine.reset()
    game = machine.run(reset=False)
    board = DoubleDict()
    while True:
        try:
            x, y, tile_id = [next(game) for _ in range(3)]
            board[x, y] = elements[tile_id]
        except StopIteration:
            break
    return board


def find_final_score(board, machine):
    machine.reset()
    game = machine.run(reset=False)
    score = 0
    while True:
        try:
            x, y, tile_id = [next(game) for _ in range(3)]
            if (x, y) == (-1, 0):
                score = tile_id
            else:
                board[x, y] = elements[tile_id]
                if tile_id == 4:
                    ball, paddle = board.index("ball"), board.index("paddle")
                    move = 0
                    if ball[0] < paddle[0]:
                        move = -1
                    elif ball[0] > paddle[0]:
                        move = 1
                    machine.send(move)
        except StopIteration:
            return score


def part_one():
    return Counter(initialise(arcade).values())["block"]


def part_two():
    return find_final_score(initialise(arcade), play_arcade)


print(part_one())  # 205
print(part_two())  # 10292
