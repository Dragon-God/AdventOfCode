with open(r"..\Inputs\day_3.txt") as file:
    wires = [line.rstrip().split(",") for line in file.readlines()]


def dist(p1: tuple, p2=(0, 0): tuple) -> int:
    """Calculates the Manhattan distance between two points"""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def trace(step: str, pos: tuple) -> list:
    """Draws the line formed by applying a step (`step`) to a given coordinate (`pos`).
    
        Args:
            `step`: The step to be taken.
            `pos`: The position to which the step should be applied.
        Returns:
            (list): A list of coordinates that define the line.
    """
    shift = int(step[1:])
    direction = step[0]
    x = pos[0]
    y = pos[1]
    if direction == "D":
        line = [(x, y-j) for j in range(1, shift+1)]
    elif direction == "U":
        line = [(x, y+j) for j in range(1, shift+1)]
    elif direction == "L":
        line = [(x-i, y) for i in range(1, shift+1)]
    elif direction == "R":
        line = [(x+i, y) for i in range(1, shift+1)]
    return line


def draw(pos: tuple, path: list) -> list:
    """Draws the graph formed by following a sequence of steps (`path`) from a given starting position (`pos`)."""
    graph = []
    for step in path:
        line = trace(step, pos)
        pos = line[-1]  # Update `pos`.
        graph += line
    return graph


def intersect(paths: list) -> tuple:
    """Draws the graphs formed by following the two provided paths and finds their intersection.
    
        Args:
            `paths`: A list of two elements, corresponding to the paths for the two wires.
        Returns:
            (tuple): A 3-tuple representing the graphs of the three wires and their intersections.
                `graph_1 (list)`: Graph of the first wire.
                `graph_2 (list)`: Graph of the second wire.
                `crosses`: Set of points where the two wires cross each other.
    """
    graph_1, graph_2 = draw((0, 0), paths[0]), draw((0, 0), paths[1])
    crosses = set(graph_1) & set(graph_2)
    return crosses, graph_1, graph_2


def reaches(paths: list) -> dict:
    """Finds the distance travelled by each wire to their various points of intersection.
    
        Args:
            `paths`: A list of two elements, corresponding to the paths for the two wires.
        Returns:
            (dict): A dictionary mapping each point of intersection to the distances the two wires take to reach it.
    """
    crosses, graph_1, graph_2 = intersect(paths)
    dct = {point: [None, None] for point in crosses}
    for idx, pair in enumerate(graph_1):
        if pair in crosses:
            dct[pair][0] = dct[pair][0] or idx+1
    for idx, pair in enumerate(graph_2):
        if pair in crosses:
            dct[pair][1] = dct[pair][1] or idx+1
    return dct


def part_one() -> int:
    """Finds minimum Manhattan distance from origin of the intersection points."""
    return min(dist(cross) for cross in intersect(wires)[0])


def part_two() -> int:
    """Finds minimum distance travelled by the two wires to reach an intersection point."""
    return min(sum(pair) for pair in reaches(wires).values())
