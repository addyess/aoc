from functools import partial
from itertools import product


class Ins:
    @classmethod
    def parse(cls, line):
        cmd, *args = line.strip().split(' ')
        return cls(cmd, *args)

    def __init__(self, operation, *args):
        self.run = partial(getattr(self, operation))
        self.args = args

    def __repr__(self):
        return f"{self.run.func.__name__} {' '.join(self.args)}"

    def inp(self, machine, input_buffer):
        machine.registers[self.args[0]] = int(next(input_buffer))

    def _dref(self, machine):
        b = self.args[1]
        if b in 'wxyz':
            b = machine.registers[b]
        else:
            b = int(b)
        return b

    def add(self, machine, *_args):
        machine.registers[self.args[0]] += self._dref(machine)

    def mul(self, machine, *_args):
        machine.registers[self.args[0]] *= self._dref(machine)

    def div(self, machine, *_args):
        machine.registers[self.args[0]] //= self._dref(machine)

    def mod(self, machine, *_args):
        machine.registers[self.args[0]] %= self._dref(machine)

    def eql(self, machine, *_args):
        machine.registers[self.args[0]] = int(machine.registers[self.args[0]] == self._dref(machine))


class Machine:
    @classmethod
    def parse(cls, lines):
        return cls([Ins.parse(line) for line in lines])

    def __init__(self, ins):
        self.ins = ins
        self.registers = dict(w=0, x=0, y=0, z=0)
        self.state = []

    def __repr__(self):
        return str(self.registers)

    def duplicate(self):
        return Machine(self.ins)

    def run(self, _input):
        it = iter(_input)
        for idx, ins in enumerate(self.ins):
            self.state.append(dict(self.registers))
            ins.run(self, it)
        return self


with open('day24.txt') as fin:
    monad = Machine.parse(fin)

gen = ((p, monad.duplicate().run(p)) for p in product('987654321', repeat=14))
val = next(p for p, val in gen if val == 0)
print(f"Result #1 {val}")