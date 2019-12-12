import numpy as np
from math import gcd
from math import atan2
from math import pi
from collections import defaultdict
from collections import deque
import os

os.chdir(r"2019\Solutions")

with open(r"..\Inputs\day_10.txt") as file:
    grid = np.array([[1 if x == "#" else 0 for x in line]
                     for line in file.readlines()]).transpose()

x_length, y_length = grid.shape  # pylint: disable=w0633
asteroids = [(x, y) for x in range(x_length)
             for y in range(y_length) if grid[x, y] == 1]


def base_offset(ref, coord):
    x, y = coord[0] - ref[0], ref[1] - coord[1]
    div = gcd(x, y)
    if x == 0:
        return 0, 1 if y > 0 else -1
    elif y == 0:
        return 1 if x > 0 else -1, 0
    return x//div, y//div


def monitors(asteroids):
    for ref in asteroids:
        dct = defaultdict(lambda: [])
        for coord in (x for x in asteroids if x != ref):
            offset = base_offset(ref, coord)
            dct[offset] = dct[offset] + [coord]
        yield ref, dct


station, dists = max(monitors(asteroids), key=lambda x: len(x[1]))


def man_dist(p1, p2):
    return abs((p1[0] - p2[0])) + abs((p1[1] - p2[1]))


def eliminated_order(distances, ref):
    dct = distances.copy()
    for key in dct.keys():
        dct[key] = deque(sorted(dct[key], key=lambda x: man_dist(x, ref)))
    keys = sorted(dct.keys(), key=lambda x: atan2(*x)
                  if atan2(*x) >= 0 else 2*pi + atan2(*x))
    result = []
    while dct:
        for offset in keys:
            if dct[offset]:
                result.append(dct[offset].popleft())
            else:
                del dct[offset]
    return result


def part_one():
    return len(dists)


def part_two():
    x, y = eliminated_order(dists, station)[199]
    return x*100 + y


print(part_one())  # 329
print(part_two())  # 512
