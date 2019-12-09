from itertools import cycle
from itertools import permutations as perm
import os

from statemachine import StateMachine, operators

os.chdir(r"2019\Solutions")

with open(r"../Inputs/day_7.txt") as file:
    program = [int(i) for i in file.read().split(",")]


def amplify(init, program, num):
    machine = StateMachine(operators, program)
    for tpl in perm(range(num)):
        output = init
        for signal in tpl:
            machine.send([signal, output])
            output = next(machine.run())
            machine.reset()
        yield output


def chained_amplify(init, program, lower, upper):
    upper += 1
    machines = [StateMachine(operators, program) for _ in range(lower, upper)]
    for tpl in perm(range(lower, upper)):
        output = init
        amps = cycle([machine.run(False) for machine in machines])
        for idx, (signal, machine) in enumerate(zip(tpl, machines)):
            machine.send([signal])
        machine_cycle = cycle([machine for machine in machines])
        for amp, machine in zip(amps, machine_cycle):
            try:
                machine.send([output])
                output = next(amp)
            except StopIteration:
                break
        [machine.reset() for machine in machines]
        yield output


def part_one():
    return max(amplify(0, program, 5))


def part_two():
    return max(chained_amplify(0, program, 5, 9))


print(part_one())  # 17406
print(part_two())  # 1047153
