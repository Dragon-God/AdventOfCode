# Advent of Code 2019: Day 1
  
I'm doing [Advent of Code](https://adventofcode.com/) this year. Below is my attempt at [day 1](https://adventofcode.com/2019/day/1):  
  
## Problem  

### Part One

> --- Day 1: The Tyranny of the Rocket Equation ---

> Santa has become stranded at the edge of the Solar System while delivering presents to other planets! To accurately calculate his position in space, safely align his warp drive, and return to Earth in time to save Christmas, he needs you to bring him measurements from fifty stars.

> Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

> The Elves quickly load you into a spacecraft and prepare to launch.

> At the first Go / No Go poll, every Elf is Go until the Fuel Counter-Upper. They haven't determined the amount of fuel required yet.

> Fuel required to launch a given module is based on its mass. Specifically, to find the fuel required for a module, take its mass, divide by three, round down, and subtract 2.

> For example:

> - For a mass of 12, divide by 3 and round down to get 4, then subtract 2 to get 2.
> - For a mass of 14, dividing by 3 and rounding down still yields 4, so the fuel required is also 2.
> - For a mass of 1969, the fuel required is 654.
> - For a mass of 100756, the fuel required is 33583.

> The Fuel Counter-Upper needs to know the total fuel requirement. To find it, individually calculate the fuel needed for the mass of each module (your puzzle input), then add together all the fuel values.

> What is the sum of the fuel requirements for all of the modules on your spacecraft?

&nbsp;  

### Part Two

> --- Part Two ---

> During the second Go / No Go poll, the Elf in charge of the Rocket Equation Double-Checker stops the launch sequence. Apparently, you forgot to include additional fuel for the fuel you just added.

> Fuel itself requires fuel just like a module - take its mass, divide by three, round down, and subtract 2. However, that fuel also requires fuel, and that fuel requires fuel, and so on. Any mass that would require negative fuel should instead be treated as if it requires zero fuel; the remaining mass, if any, is instead handled by wishing really hard, which has no mass and is outside the scope of this calculation.

> So, for each module mass, calculate its fuel and add it to the total. Then, treat the fuel amount you just calculated as the input mass and repeat the process, continuing until a fuel requirement is zero or negative. For example:

> - A module of mass 14 requires 2 fuel. This fuel requires no further fuel (2 divided by 3 and rounded down is 0, which would call for a negative fuel), so the total fuel required is still just 2.
> - At first, a module of mass 1969 requires 654 fuel. Then, this fuel requires 216 more fuel (654 / 3 - 2). 216 then requires 70 more fuel, which requires 21 fuel, which requires 5 fuel, which requires no further fuel. So, the total fuel required for a module of mass 1969 is 654 + 216 + 70 + 21 + 5 = 966.
> - The fuel required by a module of mass 100756 and its fuel is: 33583 + 11192 + 3728 + 1240 + 411 + 135 + 43 + 12 + 2 = 50346.

> What is the sum of the fuel requirements for all of the modules on your spacecraft when also taking into account the mass of the added fuel? (Calculate the fuel requirements for each module separately, then add them all up at the end.)
  
___
  
## Solution

```python
f = lambda mass: mass // 3 - 2

def partial_sum(mass):
    return 0 if f(mass) <= 0 else f(mass) + partial_sum(f(mass))


def part_one():
    with open(r"..\Inputs\day_1.txt") as file:
        return sum(f(int(i)) for i in file.readlines())

def part_two():
    with open(r"..\Inputs\day_1.txt") as file:
        return sum(partial_sum(int(mass)) for mass in file.readlines())
```
  
___
  
## Notes

I don't consider myself a beginner in Python, however I am not proficient in it either. I guess I would be at the lower ends of intermediate. I am familiar with PEP 8 and have read it in its entirety, thus, any stylistic deviations I make are probably deliberate. Nevertheless, feel free to point them out if you feel a particular choice of mine was sufficiently erroneous. I am concerned with best practices and readability, but also the performance of my code. I am not sure what tradeoff is appropriate, and would appreciate feedback on the tradeoffs I did make.  
  
My style tends to over utilise functions. This is partly because I genuinely think separating functionality into functions is a good thing, but is also an artifiact of my development practices. I tend to write the program in a Jupyter notebook (the ability to execute arbitrary code excerpts in semi isolated cells is a very helpful development aid and lends itself naturally to one function per cell (with the added benefit of being able to easily test functions independently)). I would welcome thoughts on this, but unless it is particularly egregious, I am unlikely to change it.
