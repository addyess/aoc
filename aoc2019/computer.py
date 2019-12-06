from collections import defaultdict


def halt(_):
    return lambda _: True


def add(modes, a, b, c):
    def exec(machine):
        va = a if modes[0] else machine.locs[a]
        vb = b if modes[1] else machine.locs[b]
        machine.locs[c] = va + vb
    return exec


def mul(modes, a, b, c):
    def exec(machine):
        va = a if modes[0] else machine.locs[a]
        vb = b if modes[1] else machine.locs[b]
        machine.locs[c] = va * vb
    return exec


def op_input(_, a):
    def exec(machine):
        try:
            v = next(machine.stdin)
        except StopIteration:
            v = int(input("int: "))
        machine.locs[a] = v
    return exec


def op_output(modes, a):
    def exec(machine):
        va = a if modes[0] else machine.locs[a]
        try:
            machine.stdout.append(va)
        except AttributeError:
            print(f"out: {va}")
    return exec


def jump_if_true(modes, a, b):
    def exec(machine):
        va = a if modes[0] else machine.locs[a]
        vb = b if modes[1] else machine.locs[b]
        if va != 0:
            machine.pc = vb
    return exec


def jump_if_false(modes, a, b):
    def exec(machine):
        va = a if modes[0] else machine.locs[a]
        vb = b if modes[1] else machine.locs[b]
        if va == 0:
            machine.pc = vb
    return exec


def less_than(modes, a, b, c):
    def exec(machine):
        va = a if modes[0] else machine.locs[a]
        vb = b if modes[1] else machine.locs[b]
        machine.locs[c] = int(va < vb)
    return exec


def equality(modes, a, b, c):
    def exec(machine):
        va = a if modes[0] else machine.locs[a]
        vb = b if modes[1] else machine.locs[b]
        machine.locs[c] = int(va == vb)
    return exec


def param_modes(opcode):
    modes = opcode//100
    i = 0
    while modes:
        modes, m = modes // 10, modes % 10
        yield i, bool(m)
        i += 1


def make_op(locs):
    inst, locs = locs[0], locs[1:]
    opcode = inst % 100
    if opcode == 1 and len(locs) >= 3:
        params, op = 3, add
    elif opcode == 2 and len(locs) >= 3:
        params, op = 3, mul
    elif opcode == 3 and len(locs) >= 1:
        params, op = 1, op_input
    elif opcode == 4 and len(locs) >= 1:
        params, op = 1, op_output
    elif opcode == 5 and len(locs) >= 2:
        params, op = 2, jump_if_true
    elif opcode == 6 and len(locs) >= 2:
        params, op = 2, jump_if_false
    elif opcode == 7 and len(locs) >= 3:
        params, op = 3, less_than
    elif opcode == 8 and len(locs) >= 3:
        params, op = 3, equality
    else:
        params, op = 0, halt
    modes = defaultdict(int, {k: v for k, v in param_modes(inst)})
    head, locs = locs[0:params], locs[params:]
    return params+1, op(modes, *head)


class Machine:
    def __init__(self, locs):
        self.pc, self.locs = 0, locs
        self.stdin, self.stdout = None, []

    @classmethod
    def decode(cls, intcode):
        locs = [int(_) for _ in intcode.split(",")]
        return cls(locs)

    def step(self):
        next_pc, next_op = make_op(self.locs[self.pc:])
        self.pc += next_pc
        return next_op(self)

    def run(self, stdin=None, stdout=None):
        try:
            self.stdin = iter(stdin)
        except TypeError:
            self.stdin = iter([])
        if stdout:
            self.stdout = stdout
        while not self.step():
            pass
        return self.stdout
