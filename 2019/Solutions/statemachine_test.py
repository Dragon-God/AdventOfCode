from itertools import cycle
from itertools import permutations as perm
import os

from statemachine import StateMachine, operators

os.chdir(r"2019\Solutions")

with open(r"..\Inputs\day_5.txt") as file:
    program_5 = [int(i) for i in file.read().split(",")]

machine_5 = StateMachine(operators, program_5)


def five_part_one():
    machine_5.send(1)
    return list(machine_5.run()).pop()


def five_part_two():
    machine_5.send(5)
    return list(machine_5.run()).pop()


with open(r"..\Inputs\day_7.txt") as file:
    program_7 = [int(i) for i in file.read().split(",")]


def amplify(init, program, num):
    machine = StateMachine(operators, program)
    for tpl in perm(range(num)):
        output = init
        for signal in tpl:
            machine.send(signal, output)
            output = next(machine.run())
            machine.reset()
        yield output


def chained_amplify(init, program, lower, upper):
    upper += 1
    machines = [StateMachine(operators, program) for _ in range(lower, upper)]
    for tpl in perm(range(lower, upper)):
        output = init
        amps = cycle([machine.run(False) for machine in machines])
        for signal, machine in zip(tpl, machines):
            machine.send(signal)
        machine_cycle = cycle([machine for machine in machines])
        for amp, machine in zip(amps, machine_cycle):
            try:
                machine.send(output)
                output = next(amp)
            except StopIteration:
                break
        [machine.reset() for machine in machines]
        yield output


def seven_part_one():
    return max(amplify(0, program_7, 5))


def seven_part_two():
    return max(chained_amplify(0, program_7, 5, 9))


with open(r"..\Inputs\day_9.txt") as file:
    program_9 = [int(i) for i in file.read().split(",")]

machine = StateMachine(operators, program_9)


def nine_part_one():
    machine.send(1)
    return list(machine.run()).pop()


def nine_part_two():
    machine.send(2)
    return list(machine.run()).pop()


print(five_part_one())  # 11049715
print(five_part_two())  # 2140710

print(seven_part_one())  # 17406
print(seven_part_two())  # 1047153

print(nine_part_one())  # 3280416268
print(nine_part_two())  # 80210
