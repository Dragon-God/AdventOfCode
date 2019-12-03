with open(r"..\Inputs\day_3.txt") as file:
    wires = [line.rstrip().split(",") for line in file.readlines()]


def dist(p1, p2=(0, 0)):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def trace(step, pos):
    shift = int(step[1:])
    if step[0] == "D":
        return [(pos[0], y) for y in range(pos[1]-1, pos[1] - shift - 1, -1)]
    elif step[0] == "U":
        return [(pos[0], y) for y in range(pos[1]+1, pos[1] + shift + 1)]
    elif step[0] == "L":
        return [(x, pos[1]) for x in range(pos[0]-1,  pos[0] - shift - 1, -1)]
    elif step[0] == "R":
        return [(x, pos[1]) for x in range(pos[0]+1,  pos[0] + shift + 1,)]

def draw(pos, path):
    graph = []
    for step in path:
        line = trace(step, pos)
        pos = line[-1]
        graph += line
    return graph

def intersect(paths):
    graph_1, graph_2 = draw((0, 0), paths[0]), draw((0, 0), paths[1])
    crosses = set(graph_1) & set(graph_2)
    return crosses, graph_1, graph_2

def reaches(paths):
    crosses, graph_1, graph_2 = intersect(paths)
    dct = {point: [None, None] for point in crosses}
    for idx, pair in enumerate(graph_1):
        if pair in crosses:
            dct[pair][0] = dct[pair][0] or idx+1
    for idx, pair in enumerate(graph_2):
        if pair in crosses:
            dct[pair][1] = dct[pair][1] or idx+1
    return dct


def part_one():
    return min(dist(cross) for cross in intersect(wires)[0])

def part_two():
    return min(sum(pair) for pair in reaches(wires).values())