from collections import defaultdict
from aoc2019.defaultlist import defaultlist
from itertools import islice


def halt(_):
    return lambda _: True


def add(modes, a, b, c):
    def exec(machine):
        va = machine.lookup(a, modes[0])
        vb = machine.lookup(b, modes[1])
        machine.store(c, modes[2], va + vb)

    return exec


def mul(modes, a, b, c):
    def exec(machine):
        va = machine.lookup(a, modes[0])
        vb = machine.lookup(b, modes[1])
        machine.store(c, modes[2], va * vb)

    return exec


def op_input(modes, a):
    def exec(machine):
        try:
            v = next(machine.stdin)
        except StopIteration:
            v = int(input("int: "))
        machine.store(a, modes[0], v)

    return exec


def op_output(modes, a):
    def exec(machine):
        va = machine.lookup(a, modes[0])
        try:
            machine.stdout.send(va)
        except (AttributeError, TypeError):
            machine.stdout.append(va)

    return exec


def jump_if_true(modes, a, b):
    def exec(machine):
        va = machine.lookup(a, modes[0])
        vb = machine.lookup(b, modes[1])
        if va != 0:
            machine.pc = vb

    return exec


def jump_if_false(modes, a, b):
    def exec(machine):
        va = machine.lookup(a, modes[0])
        vb = machine.lookup(b, modes[1])
        if va == 0:
            machine.pc = vb

    return exec


def less_than(modes, a, b, c):
    def exec(machine):
        va = machine.lookup(a, modes[0])
        vb = machine.lookup(b, modes[1])
        machine.store(c, modes[2], int(va < vb))

    return exec


def equality(modes, a, b, c):
    def exec(machine):
        va = machine.lookup(a, modes[0])
        vb = machine.lookup(b, modes[1])
        machine.store(c, modes[2], int(va == vb))

    return exec


def relative(modes, a):
    def exec(machine):
        va = machine.lookup(a, modes[0])
        machine.rb += va

    return exec


def param_modes(opcode):
    modes = opcode // 100
    i = 0
    while modes:
        modes, m = modes // 10, modes % 10
        yield i, m
        i += 1


def make_op(locs):
    inst = next(locs)
    opcode = inst % 100
    default_op = lambda: (0, halt)
    params, op = defaultdict(
        default_op, {
            1: (3, add),
            2: (3, mul),
            3: (1, op_input),
            4: (1, op_output),
            5: (2, jump_if_true),
            6: (2, jump_if_false),
            7: (3, less_than),
            8: (3, equality),
            9: (1, relative),
        })[opcode]
    modes = defaultdict(int, {k: v for k, v in param_modes(inst)})
    args = list(islice(locs, params))
    return params + 1, op(modes, *args)


class Machine:
    def __init__(self, locs, stdin, stdout):
        self.pc, self.locs = 0, locs
        self.rb = 0
        self.stdin, self.stdout = stdin, stdout

    def lookup(self, pos, mode):
        if mode == 0:  # position
            return self.locs[pos]
        elif mode == 1:  # immediate
            return pos
        elif mode == 2:  # relative
            return self.locs[pos + self.rb]
        raise NotImplementedError(f"invalid mode {mode}")

    def store(self, pos, mode, val):
        if mode == 0:  # position
            self.locs[pos] = val
        elif mode == 2:  # relative
            self.locs[pos + self.rb] = val
        else:
            raise NotImplementedError(f"invalid mode {mode}")

    @classmethod
    def decode(cls, intcode, stdin=None, stdout=None):
        locs = defaultlist(int, [int(_) for _ in intcode.split(",")])

        try:
            stdin = iter(stdin)
        except TypeError:
            stdin = iter([])

        try:
            stdout = iter(stdout)
        except TypeError:
            stdout = []

        return cls(locs, stdin, stdout)

    def step(self):
        next_pc, next_op = make_op(islice(self.locs, self.pc, None))
        self.pc += next_pc
        return next_op(self)

    def run(self):
        while not self.step():
            pass
        return self.stdout
