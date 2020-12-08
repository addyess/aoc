import re
try:
    from functools import cached_property
except ImportError:
    cached_property = property


class Operation:
    INS_RE = re.compile(r"(\S+) ([-|+]\d+)")

    def __repr__(self):
        return f"{type(self).__name__}({','.join(self.args)})"

    def __init__(self, *args):
        self.args = args

    @cached_property
    def arg0(self):
        return int(self.args[0])

    @classmethod
    def parsed(cls, stream):
        def parse(_):
            meth, val = cls.INS_RE.search(_).groups()
            return klass[meth](val)
        klass = {
            "nop": NOP,
            "acc": ACCU,
            "jmp": JMP
        }
        return [parse(_) for _ in stream]


class NOP(Operation):
    def __call__(self, machine):
        return machine.reg['pc'] + 1


class ACCU(Operation):
    def __call__(self, machine):
        machine.reg['acc'] += self.arg0
        return machine.reg['pc'] + 1


class JMP(Operation):
    def __call__(self, machine):
        return machine.reg['pc'] + self.arg0


class Machine:
    @classmethod
    def load(cls, ins):
        return cls(Operation.parsed(ins))

    def __init__(self, listing):
        self.listing = listing
        self.reg = {
            "acc": 0,
            "pc": 0
        }

    def step(self):
        pc = self.reg['pc']
        if pc >= len(self.listing):
            raise EOFError()
        self.reg['pc'] = self.listing[pc](self)
