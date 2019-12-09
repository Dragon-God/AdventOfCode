from itertools import combinations
import os

os.chdir(r"2019\Solutions")

with open(r"..\Inputs\day_2.txt") as file:
    lst = [int(i) for i in file.read().split(",")]


def compute(lst):
    idx = 0
    while True:
        if lst[idx] == 1:
            lst[lst[idx + 3]] = lst[lst[idx + 1]] + lst[lst[idx + 2]]
        elif lst[idx] == 2:
            lst[lst[idx + 3]] = lst[lst[idx + 1]] * lst[lst[idx + 2]]
        elif lst[idx] == 99:
            break
        idx += 4
    return lst[0]

def part_one():
    test = lst[:]
    test[1:3] = [12, 2]
    return compute(test)

def part_two():
    for noun, verb in combinations(range(100), 2):
        test = lst[:]
        test[1:3] = [noun, verb]
        if compute(test) == 19690720:
            return 100 * noun + verb


print(part_one())  # 3790645
print(part_two())  # 6577
