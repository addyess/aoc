class HALT(BaseException):
    def exec(self, machine):
        return False


class ADD:
    def __init__(self, a, b, c):
        self.a, self.b, self.c = a, b, c

    def exec(self, machine):
        machine.locs[self.c] = machine.locs[self.a] + machine.locs[self.b]
        return True


class MUL:
    def __init__(self, a, b, c):
        self.a, self.b, self.c = a, b, c

    def exec(self, machine):
        machine.locs[self.c] = machine.locs[self.a] * machine.locs[self.b]
        return True


def make_op(locs):
    head, locs = locs[0], locs[1:]
    if head == 1 and len(locs) >= 3:
        head, locs = locs[0:3], locs[3:]
        return 4, ADD(*head)
    elif head == 2 and len(locs) >= 3:
        head, locs = locs[0:3], locs[3:]
        return 4, MUL(*head)
    else:
        return 1, HALT()


class Machine:
    def __init__(self, locs):
        self.pc, self.locs = 0, locs

    @classmethod
    def decode(cls, intcode):
        locs = [int(_) for _ in intcode.split(",")]
        return cls(locs)

    def step(self):
        next_pc, next_op = make_op(self.locs[self.pc:])
        self.pc += next_pc
        return next_op.exec(self)

    def run(self):
        while self.step():
            pass
