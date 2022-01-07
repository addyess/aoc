import re
from collections import OrderedDict
from functools import partial
from itertools import product
from sympy import symbols, simplify, Eq, Expr

NAMEERROR_RE = re.compile("name '(\S)' is not defined")
VARIABLES = symbols(list("ABCDEFGHIJKLMN"), nonzero=True, integer=True)


class Ins:
    @classmethod
    def parse(cls, line):
        cmd, *args = line.strip().split(' ')
        return cls(cmd, *args)

    def __init__(self, operation, *args):
        self.run = partial(getattr(self, operation, self.noop))
        self.args = args

    def noop(self, *args):
        pass

    def _dref(self, machine):
        b = self.args[1]
        if b in 'wxyz':
            return machine.registers[b]
        return int(b)

    def inp(self, machine, input_buffer):
        machine.registers[self.args[0]] = next(input_buffer)

    def add(self, machine, *_args):
        reg = machine.registers[self.args[0]]
        dref = self._dref(machine)
        machine.registers[self.args[0]] = simplify(reg + dref)

    def mul(self, machine, *_args):
        reg = machine.registers[self.args[0]]
        dref = self._dref(machine)
        machine.registers[self.args[0]] = simplify(reg * dref)

    def div(self, machine, *_args):
        reg = machine.registers[self.args[0]]
        dref = self._dref(machine)
        machine.registers[self.args[0]] = simplify(reg // dref)

    def mod(self, machine, *_args):
        reg = machine.registers[self.args[0]]
        dref = self._dref(machine)
        machine.registers[self.args[0]] = simplify(reg % dref)

    def eql(self, machine, *_args):
        def int_len_too_long(val):
            try:
                return len(str(int(val))) > 1
            except (ValueError, TypeError):
                pass

        reg = machine.registers[self.args[0]]
        dref = self._dref(machine)
        if reg in VARIABLES and int_len_too_long(dref):
            r = 0
        elif dref in VARIABLES and int_len_too_long(reg):
            r = 0
        else:
            eq = Eq(reg, dref)
            if eq == True:
                r = 1
            elif eq == False:
                r = 0
            else:
                r = self.reduce(eq, machine)
        machine.registers[self.args[0]] = r

    @staticmethod
    def reduce(equality: Expr, machine, give_options=False):
        symbols = sorted(equality.free_symbols, key=lambda s: s.name)
        new_options = {s: set() for s in symbols}
        choice_sets = [(v, machine.options[v]) for v in symbols]

        def replacements():
            for opts in product(*OrderedDict(choice_sets).values()):
                yield {choice_sets[k][0]: v for k, v in enumerate(opts)}

        for rep in replacements():
            if equality.subs(rep) == True:
                for s, v in rep.items():
                    new_options[s] |= {v}

        if give_options:
            return new_options

        if not any(new_options.values()):
            return 0
        else:
            for v, opts in new_options.items():
                machine.options[v] &= opts
            return 1


class Machine:
    @classmethod
    def parse(cls, lines):
        return cls([Ins.parse(line) for line in lines])

    def __init__(self, ins):
        self.ins = ins
        self.registers = dict(w=0, x=0, y=0, z=0)
        self.options = OrderedDict(
            (v, set(range(1, 10)))
            for v in VARIABLES
        )

    def train(self, serial=VARIABLES):
        it = iter(serial)
        for idx, ins in enumerate(self.ins):
            ins.run(self, it)
        return self

    def eval_z(self):
        expr = Eq(self.registers['z'], 0)
        Ins.reduce(expr, self)
        max_serial = "".join([str(max(_)) for _ in self.options.values()])
        min_serial = "".join([str(min(_)) for _ in self.options.values()])
        return max_serial, min_serial


with open('day24.txt') as fin:
    monad = Machine.parse(fin)
res1, res2 = monad.train(VARIABLES).eval_z()
print(f"Result #1 {res1}")
print(f"Result #2 {res2}")
