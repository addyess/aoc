import math
from collections import defaultdict
from itertools import count


class Equation:
    @staticmethod
    def amt_chem(dep):
        n, chem = dep.strip().split(' ')
        return int(n), chem

    @classmethod
    def from_line(cls, line):
        react, chem = line.split(' => ')
        return cls([cls.amt_chem(dep) for dep in react.split(',')], *cls.amt_chem(chem))

    def as_tuple(self):
        return self.chem, self

    def __init__(self, deps, amt, chem):
        self.amt = amt
        self.chem = chem
        self.deps = deps


class System:
    @classmethod
    def main(cls, rules):
        d = dict(map(Equation.as_tuple, [Equation.from_line(line) for line in rules.splitlines()]))
        return cls(d)

    def __init__(self, rules):
        self.rules = rules
        self.pool = defaultdict(int)
        self.created = defaultdict(int)

    def exhaust_ore(self, ore):
        self.pool['ORE'] = ore
        for fuel in count():
            if self.pool['ORE'] < self.created['ORE']:
                return fuel - 1
            self.to_produce(1, 'FUEL')
            self.pool['ORE'] -= self.created['ORE']
            self.created['ORE'] = 0
        return 0

    def to_produce(self, need, elem):
        if elem == 'ORE':
            self.created[elem] += need
            return

        if self.pool[elem] >= need:
            self.pool[elem] -= need
            return

        new_demand = need - self.pool[elem]
        equ = self.rules[elem]
        multiplier = math.ceil(new_demand / equ.amt)
        [self.to_produce(amt*multiplier, name) for amt, name in equ.deps]
        created = equ.amt * multiplier
        self.created[elem] += created
        self.pool[elem] = created - new_demand


with open("day14.txt") as fin:
    ins = fin.read()
system = System.main(ins)
system.to_produce(1, 'FUEL')
print(f"Result 1: {system.created['ORE']}")

system = System.main(ins)
print(f"Result 2: {system.exhaust_ore(1000000000000)}")
