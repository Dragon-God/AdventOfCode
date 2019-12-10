# Advent of Code 2019: Day 4
  
I'm doing [Advent of Code](https://adventofcode.com/) this year. Below is my attempt at [day 4](https://adventofcode.com/2019/day/4):  
  
## Problem  

### Part One

> --- Day 4: Secure Container ---

> You arrive at the Venus fuel depot only to discover it's protected by a password. The Elves had written the password on a sticky note, but someone threw it out.

> However, they do remember a few key facts about the password:

> - It is a six-digit number.
> - The value is within the range given in your puzzle input.
> - Two adjacent digits are the same (like `22` in `122345`).
> - Going from left to right, the digits never decrease; they only ever increase or stay the same (like `111123` or `135679`).

> Other than the range rule, the following are true:

> - `111111` meets these criteria (double `11`, never decreases).
> - `223450` does not meet these criteria (decreasing pair of digits `50`).
> - `123789` does not meet these criteria (no double).

> How many different passwords within the range given in your puzzle input meet these criteria?


&nbsp;  

### Part Two

> --- Part Two ---

> An Elf just remembered one more important detail: the two adjacent matching digits are not part of a larger group of matching digits.

> Given this additional criterion, but still ignoring the range rule, the following are now true:

> - `112233` meets these criteria because the digits never decrease and all repeated digits are exactly two digits long.
> - `123444` no longer meets the criteria (the repeated `44` is part of a larger group of `444`).
> - `111122` meets the criteria (even though `1` is repeated more than twice, it still contains a double `22`).

> How many different passwords within the range given in your puzzle input meet all of the criteria?
  
___
  
## Solution

```python
from itertools import groupby

bounds = (265275, 781584)

rules = [
    # Digits are never decreasing
    lambda s: all(int(s[i]) <= int(s[i+1])
                  for i in range(len(s)-1)),
    # Two adjacent digits are equal.
    lambda s: any(s[i] == s[i+1] for i in range(len(s)-1)),
    # Two adjacent digits don't form a larger group.
    lambda s: any(len(list(v)) == 2 for _, v in groupby(s))
]


def test(num, rules):
    return all(f(str(num)) for f in rules)


def solve(bounds, rules):
    return sum(1 for i in range(bounds[0], bounds[1]+1) if test(i, rules))


def part_one():
    return solve(bounds, rules[:2])


def part_two():
    return solve(bounds, rules[::2])


print(part_one())  # 960
print(part_two())  # 626

```
  
___
  
## Notes

I don't consider myself a beginner in Python, however I am not proficient in it either. I guess I would be at the lower ends of intermediate. I am familiar with PEP 8 and have read it in its entirety, thus, any stylistic deviations I make are probably deliberate. Nevertheless, feel free to point them out if you feel a particular choice of mine was sufficiently erroneous. I am concerned with best practices and readability, but also the performance of my code. I am not sure what tradeoff is appropriate, and would appreciate feedback on the tradeoffs I did make.  
  
My style tends to over utilise functions. This is partly because I genuinely think separating functionality into functions is a good thing, but is also an artifiact of my development practices. I tend to write the program in a Jupyter notebook (the ability to execute arbitrary code excerpts in semi isolated cells is a very helpful development aid and lends itself naturally to one function per cell (with the added benefit of being able to easily test functions independently)). I would welcome thoughts on this, but unless it is particularly egregious, I am unlikely to change it.
