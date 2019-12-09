import operator as op
import os

from statemachine import StateMachine, operators

os.chdir(r"2019\Solutions")

with open(r"..\Inputs\day_5.txt") as file:
    program = [int(i) for i in file.read().split(",")]

machine = StateMachine(operators, program)


def part_one():
    machine.send([1])
    return list(machine.run()).pop()


def part_two():
    machine.send([5])
    return list(machine.run()).pop()


print(part_one())   # 11049715
print(part_two())   # 2140710
