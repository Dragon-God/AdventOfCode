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