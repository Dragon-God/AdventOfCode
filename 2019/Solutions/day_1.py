f = lambda mass: mass // 3 - 2

def part_one():
  with open(r"../Inputs/day_1.txt") as file:
    return sum(f(int(i)) for i in file.readlines())

def part_two():
  def partial_sum(mass):
    return 0 if f(mass) <= 0 else f(mass) + partial_sum(f(mass))
  with open(r"../Inputs/day_1.txt") as file:
    return sum(partial_sum(int(mass)) for mass in file.readlines())