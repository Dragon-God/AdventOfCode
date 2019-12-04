# Advent of Code 2019: Day 3
  
I'm doing [Advent of Code](https://adventofcode.com/) this year. Below is my attempt at [day 3](https://adventofcode.com/2019/day/3):  
  
## Problem  

### Part One

> --- Day 3: Crossed Wires ---

> The gravity assist was successful, and you're well on your way to the Venus refuelling station. During the rush back on Earth, the fuel management system wasn't completely installed, so that's next on the priority list.

> Opening the front panel reveals a jumble of wires. Specifically, two wires are connected to a central port and extend outward on a grid. You trace the path each wire takes as it leaves the central port, one wire per line of text (your puzzle input).

> The wires twist and turn, but the two wires occasionally cross paths. To fix the circuit, you need to _find the intersection point closest to the central port_. Because the wires are on a grid, use the [Manhattan distance](https://en.wikipedia.org/wiki/Taxicab_geometry) for this measurement. While the wires do technically cross right at the central port where they both start, this point does not count, nor does a wire count as crossing with itself.

> For example, if the first wire's path is `R8,U5,L5,D3`, then starting from the central port (`o`), it goes right `8`, up `5`, left `5`, and finally down `3`:

> 
```
...........
...........
...........
....+----+.
....|....|.
....|....|.
....|....|.
.........|.
.o-------+.
...........
```

> Then, if the second wire's path is `U7,R6,D4,L4`, it goes up `7`, right `6`, down `4`, and left `4`:

> 
```
...........
.+-----+...
.|.....|...
.|..+--X-+.
.|..|..|.|.
.|.-X--+.|.
.|..|....|.
.|.......|.
.o-------+.
...........
```

> These wires cross at two locations (marked `X`), but the lower-left one is closer to the central port: its distance is `3 + 3 = 6`.

> Here are a few more examples:

> - `R75,D30,R83,U83,L12,D49,R71,U7,L72`  
    `U62,R66,U55,R34,D71,R55,D58,R83` = distance `159`

> - `R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51`  
    `U98,R91,D20,R16,D67,R40,U7,R15,U6,R7` = distance `135`

> _What is the Manhattan distance_ from the central port to the closest intersection?

&nbsp;  

### Part Two

> --- Part Two ---

> It turns out that this circuit is very timing-sensitive; you actually need to _minimize the signal delay_.

> To do this, calculate the _number of steps_ each wire takes to reach each intersection; choose the intersection where the _sum of both wires' steps_ is lowest. If a wire visits a position on the grid multiple times, use the steps value from the _first_ time it visits that position when calculating the total value of a specific intersection.

> The number of steps a wire takes is the total number of grid squares the wire has entered to get to that location, including the intersection being considered. Again consider the example from above:

> 
```
...........
.+-----+...
.|.....|...
.|..+--X-+.
.|..|..|.|.
.|.-X--+.|.
.|..|....|.
.|.......|.
.o-------+.
...........
```

> In the above example, the intersection closest to the central port is reached after `8+5+5+2 = 20` steps by the first wire and `7+6+4+3 = 20` steps by the second wire for a total of `20+20 = 40` steps.

> However, the top-right intersection is better: the first wire takes only `8+5+2 = 15` and the second wire takes only `7+6+2 = 15`, a total of `15+15 = 30` steps.

> Here are the best steps for the extra examples from above:

> - `R75,D30,R83,U83,L12,D49,R71,U7,L72`  
    `U62,R66,U55,R34,D71,R55,D58,R83` = `610` steps
> - `R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51`  
    `U98,R91,D20,R16,D67,R40,U7,R15,U6,R7` = `410` steps

> _What is the fewest combined steps the wires must take to reach an intersection?_

  
___
  
## Solution

```python
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
```
  
___
  
## Notes

I don't consider myself a beginner in Python, however I am not proficient in it either. I guess I would be at the lower ends of intermediate. I am familiar with PEP 8 and have read it in its entirety, thus, any stylistic deviations I make are probably deliberate. Nevertheless, feel free to point them out if you feel a particular choice of mine was sufficiently erroneous. I am concerned with best practices and readability, but also the performance of my code. I am not sure what tradeoff is appropriate, and would appreciate feedback on the tradeoffs I did make.  

For example, `reaches()` could have been rewritten as:
```python
def reaches(paths: list) -> dict:
    """Finds the distance travelled by each wire to their various points of intersection.
    
        Args:
            `paths`: A list of two elements, corresponding to the paths for the two wires.
        Returns:
            (dict): A dictionary mapping each point of intersection to the distances the two wires take to reach it.
    """
    crosses, graph_1, graph_2 = intersect(paths)
    dct = {point: [None, None] for point in crosses}
    ln_1, ln_2 = len(graph_1), len(graph_2)
    if ln_1 < ln_2:
        graph_1 += [None] * (ln_2 - ln_1)
    else:
        graph_2 += [None] * (ln_1 - ln_2)
    for idx, pair in enumerate(zip(graph_1, graph_2)):
        if pair[0] in crosses:
            dct[pair[0]][0] = dct[pair[0]][0] or idx+1
        if pair[1] in crosses:
            dct[pair[1]][1] = dct[pair[1]][1] or idx+1
    return dct
```

Which eliminates one iteration and could be more performant (actual testing in my Jupyter notebook with `%timeit` did show a slight performance improvement (mean of 616 ms vs 592 ms), but I'm not sure it was significant), but might make the code less readable? I wasn't sure which tradeoff to make here.
  
My style tends to over utilise functions. This is partly because I genuinely think separating functionality into functions is a good thing, but is also an artifiact of my development practices. I tend to write the program in a Jupyter notebook (the ability to execute arbitrary code excerpts in semi isolated cells is a very helpful development aid and lends itself naturally to one function per cell (with the added benefit of being able to easily test functions independently)). I would welcome thoughts on this, but unless it is particularly egregious, I am unlikely to change it.

I am aware that the approach I took to solving this problem is not necessarily the most efficient (especially space wise), as each line could be represented by its start and end coordinates (and not as a list of all its coordinates), but I haven't worked out a satisfactory solution using that approach, so this is all I have for now.
