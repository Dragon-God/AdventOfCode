from dataclasses import dataclass
from itertools import combinations as comb
from math import gcd
from functools import reduce
import os

os.chdir(r"2019\Solutions")

with open(r"..\Inputs\day_12.txt") as file:
    initial_positions = [tuple(int(s.strip("xyz= ")) for s in line.strip(
        "\n<>").split(",")) for line in file.readlines()]

def lcm(*args):
    def f(a, b):
        return a*b//gcd(a, b)
    return reduce(f, args)


moon_names = ("Io", "Europa", "Ganymede", "Callisto")


@dataclass
class Moon:
    pos: tuple
    vel: tuple = (0, 0, 0)

    def copy(self):
        return Moon(self.pos, self.vel)


class MoonSystem(dict):
    def get_axis(self, ax):
        return {name: (moon.pos[ax], moon.vel[ax]) for name, moon in self.items()}

    def copy(self):
        return MoonSystem(zip(self.keys(), (moon.copy() for moon in self.values())))


class PlanetarySystem:
    def __init__(self, moons):
        self.initial = moons
        self.current = self.initial.copy()
        self.time = 0

    def reset(self):
        self.current = self.initial.copy()
        self.time = 0

    def update_velocity(self):
        for moon_i, moon_j in comb(self.current.values(), 2):
            vel_i, vel_j = list(moon_i.vel), list(moon_j.vel)
            for k in range(3):
                if moon_i.pos[k] > moon_j.pos[k]:
                    vel_i[k] -= 1
                    vel_j[k] += 1
                elif moon_i.pos[k] < moon_j.pos[k]:
                    vel_i[k] += 1
                    vel_j[k] -= 1
            moon_i.vel = vel_i
            moon_j.vel = vel_j

    def update_position(self):
        for moon in self.current.values():
            moon.pos = tuple(a+b for a, b in zip(moon.pos, moon.vel))

    def run(self, n=1, reset=True):
        if reset:
            self.reset()
        for _ in range(n):
            self.update_velocity()
            self.update_position()
            self.time += 1

    def kinetic_energy(self):
        return (sum(abs(x) for x in moon.vel) for moon in self.current.values())

    def potential_energy(self):
        return (sum(abs(x) for x in moon.pos) for moon in self.current.values())

    def total_energy(self):
        return sum(PE*KE for PE, KE in zip(self.kinetic_energy(), self.potential_energy()))

    def find_cycle(self):
        x_0, y_0, z_0 = tuple(self.initial.get_axis(i) for i in range(3))
        l_x = l_y = l_z = 0
        self.run()
        while not all((l_x, l_y, l_z)):
            x_i, y_i, z_i = tuple(self.current.get_axis(i) for i in range(3))
            if x_i == x_0:
                l_x = l_x or self.time
            if y_i == y_0:
                l_y = l_y or self.time
            if z_i == z_0:
                l_z = l_z or self.time
            self.run(reset=False)
        return l_x, l_y, l_z

big_four = MoonSystem(zip(moon_names, (Moon(pos) for pos in initial_positions)))
Jupiter = PlanetarySystem(big_four)

def part_one():
    Jupiter.run(1000)
    return Jupiter.total_energy()


def part_two():
    return lcm(*Jupiter.find_cycle())


print(part_one())  # 10635
print(part_two())  # 583523031727256
