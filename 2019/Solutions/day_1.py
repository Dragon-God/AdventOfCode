from itertools import combinations
import os

os.chdir(r"2019\Solutions")

with open(r"..\Inputs\day_1.txt") as file:
    input_list = [int(mass) for mass in file.readlines()]

def f(mass):
        return mass // 3 - 2

def total_fuel(mass):
    return 0 if f(mass) <= 0 else f(mass) + total_fuel(f(mass))


def part_one():
        return sum(f(mass) for mass in input_list)

def part_two():
    return sum(total_fuel(mass) for mass in input_list)


print(part_one())  # 3550236
print(part_two())  # 5322455
