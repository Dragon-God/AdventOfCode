import os
os.chdir(r"Advent of Code\2019\Solutions")

from statemachine import StateMachine, operators

with open(r"..\Inputs\day_5.txt") as file:
    program = [int(i) for i in file.read().split(",")]

machine = StateMachine(operators, program)

def part_one():
    return list(machine.run()).pop()


def part_two():
    return list(machine.run()).pop()

print(len(machine._memory))

machine.send([1])
print(part_one())  # 11049715
machine.send([5])
print(part_two())  # 2140710