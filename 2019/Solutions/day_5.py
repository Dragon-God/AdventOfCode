import operator as op

with open(r"../Inputs/day_5.txt") as file:
    input_list = [int(i) for i in file.read().split(",")]


class Operator:
    def __init__(self, code, param_length, func):
        self.code = code
        self.param_length = param_length
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


def mode(num="000"):
    return [int(x) for x in num.rjust(3, "0")[::-1]]


def modify(func):
    def wrapper(*args, memory, mode, **kwargs):
        args = [args[i] if mode[i] else memory[args[i]]
                for i in range(len(args))]
        if "input_" in kwargs:
            args = [kwargs["input_"]] + args
        result = func(*args)
        if result is not None:
            result = int(result)
        if "store" in kwargs:
            memory[kwargs["store"]] = result
        elif "output" in kwargs:
            kwargs["output"].append(result)
        else:
            return result
    return wrapper


instructions = {
    1: Operator(1, 3, modify(op.add)),
    2: Operator(2, 3, modify(op.mul)),
    3: Operator(3, 1, modify(lambda x: x)),
    4: Operator(4, 1, modify(lambda x: x)),
    5: Operator(5, 2, modify(lambda x, y: y if x else None)),
    6: Operator(6, 2, modify(lambda x, y: y if not x else None)),
    7: Operator(7, 3, modify(op.lt)),
    8: Operator(8, 3, modify(op.eq)),
    99: "halt!"
}


def parse(pos, memory):
    val = str(memory[pos])
    if len(val) > 1:
        op_ = instructions[int(val[-2:])]
        mod = mode(val[:-2])
    else:
        op_ = instructions[int(val[-1:])]
        mod = mode()
    return op_, mod


def run(input_, memory_list):
    memory = memory_list[:]
    pos = 0
    output = []
    while True:
        op_, mod = parse(pos, memory)
        if op_ == "halt!":
            return output
        next_pos = pos + op_.param_length + 1
        args = memory[pos+1:next_pos]
        kwargs = {}
        stores = [1, 2, 3, 7, 8]
        if op_.code in stores:
            kwargs["store"] = args[-1]
            args = args[:-1]
            if op_.code == 3:
                kwargs["input_"] = input_
        elif op_.code == 4:
            kwargs["output"] = output
        result = op_(*args, memory=memory, mode=mod, **kwargs)
        if result is not None:
            pos = result
        else:
            pos = next_pos
    return output


def part_one():
    return run(1, input_list)[-1]


def part_two():
    return run(5, input_list)[-1]
