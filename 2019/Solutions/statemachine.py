import operator as op
from collections import deque
from collections import defaultdict

__all__ = ["StateMachine", "operators"]


class Operator:
    def __init__(self, code, param_length, func):
        self.code = code
        self.param_length = param_length
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


def modify(func=lambda x: x):
    def wrapper(*args, memory, mode, base, **kwargs):
        args = list(args)
        for idx, arg in enumerate(args):
            mod = mode.popleft()
            if mod == 0:
                args[idx] = memory[arg]
            elif mod == 2:
                args[idx] = memory[base + arg]
        if "input_" in kwargs:
            args = [kwargs["input_"]] + args

        result = func(*args)
        if result is not None:
            result = int(result)
        if "store" in kwargs:
            if mode and mode.popleft() == 2:
                memory[base + kwargs["store"]] = result
            else:
                memory[kwargs["store"]] = result
        else:
            return result
    return wrapper


operators = {
    1: Operator(1, 3, modify(op.add)),
    2: Operator(2, 3, modify(op.mul)),
    3: Operator(3, 1, modify()),
    4: Operator(4, 1, modify()),
    5: Operator(5, 2, modify(lambda x, y: y if x else None)),
    6: Operator(6, 2, modify(lambda x, y: y if not x else None)),
    7: Operator(7, 3, modify(op.lt)),
    8: Operator(8, 3, modify(op.eq)),
    9: Operator(9, 1, modify()),
    99: "halt!"
}


class StateMachine:
    def __init__(self, operators, program):
        self.__operators = operators
        self.__program = program
        self._memory = defaultdict(lambda: 0, ((idx, val)
                                               for idx, val in enumerate(self.__program)))
        self.inputs = deque()

    def mode(self, num="000"):
        return deque([int(x) for x in num.rjust(3, "0")[::-1]])

    def parse(self, pos):
        val = str(self._memory[pos])
        if len(val) > 1:
            op_ = self.__operators[int(val[-2:])]
            mod = self.mode(val[:-2])
        else:
            op_ = self.__operators[int(val[-1:])]
            mod = self.mode()
        return op_, mod

    def reset(self):
        self._memory = defaultdict(lambda x: 0, ((idx, val)
                                                 for idx, val in enumerate(self.__program)))
        self.inputs = deque()

    def send(self, *data):
        self.inputs.extend(data)

    def run(self, reset=True):
        pos = 0
        base = 0
        while True:
            op_, mod = self.parse(pos)
            if op_ == "halt!":
                if reset:
                    self.reset()
                break
            next_pos = pos + op_.param_length + 1
            args = [self._memory[idx] for idx in range(pos+1, next_pos)]
            kwargs = {}
            stores = {1, 2, 3, 7, 8}
            jumps = {5, 6}

            if op_.code in stores:
                kwargs["store"] = args[-1]
                args = args[:-1]
                if op_.code == 3:
                    kwargs["input_"] = self.inputs.popleft()

            result = op_(*args, memory=self._memory,
                         mode=mod, base=base, **kwargs)

            if op_.code == 9:
                base += result
            elif op_.code == 4:
               yield result

            if op_.code in jumps and result is not None:
                pos = result
            else:
                pos = next_pos

    def state_test(self):
        return self._memory == defaultdict(lambda x: 0, ((idx, val)
                                                         for idx, val in enumerate(self.__program))) \
            and self.inputs == deque()
