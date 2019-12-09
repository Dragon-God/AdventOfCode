from collections import deque
import os

os.chdir(r"2019\Solutions")

with open(r"..\Inputs\day_6.txt") as file:
    input_stream = (tuple(tpl.rstrip().split(")")) for tpl in file.readlines())


class Tree:
    def __init__(self, name, ancestors=0, parent=None, children=None):
        self.name = name
        self.ancestors = ancestors
        self.parent = parent
        self.children = children or []

    def traverse(self, func):
        queue = deque([self])
        while queue:
            current = queue.popleft()
            queue.extend(current.children)
            func(current)


def inherit(tree):
    if tree.parent:
        tree.ancestors = tree.parent.ancestors + 1


def build_orbits(input_, root):
    orbits = {}
    for parent, child in input_:
        orbits[parent] = orbits.get(parent) or Tree(parent)
        if child in orbits:
            orbits[child].parent = orbits[parent]
        elif child not in orbits:
            orbits[child] = Tree(child, 1, orbits[parent])
        orbits[parent].children.append(orbits[child])
    orbits[root].traverse(inherit)
    return orbits


def count_orbits(tree):
    sm = 0

    def sum_(tree):
        nonlocal sm
        sm += tree.ancestors
    tree.traverse(sum_)
    return sm


def ancestry(tree):
    node = tree.parent
    while node:
        yield node
        node = node.parent


def find_recent_common_ancestor(source, dest, dct):
    source_a, dest_a = ancestry(source), ancestry(dest)
    common_ancestors = set(node.name for node in source_a) & set(
        node.name for node in dest_a)
    RCA = dct[max(common_ancestors, key=lambda x: dct[x].ancestors)]
    return RCA


def orbital_distance(source, dest, orbits):
    source, dest = orbits[source], orbits[dest]
    RCA = find_recent_common_ancestor(source, dest, orbits)
    return source.ancestors + dest.ancestors - 2*(RCA.ancestors + 1)


orbits = build_orbits(input_stream, "COM")


def part_one():
    return count_orbits(orbits["COM"])


def part_two():
    return orbital_distance("YOU", "SAN", orbits)


print(part_one())  # 151345
print(part_two())  # 391
