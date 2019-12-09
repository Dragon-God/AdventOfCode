import os

from statemachine import StateMachine, operators

os.chdir(r"2019\Solutions")

with open(r"..\Inputs\day_9.txt") as file:
    program = [int(i) for i in file.read().split(",")]

machine = StateMachine(operators, program)


def part_one():
    machine.send([1])
    return list(machine.run()).pop()


def part_two():
    machine.send([2])
    return list(machine.run()).pop()


print(part_one())  # 3280416268
print(part_two())  # 80210
