"""requires python3.8. for f-strings and walrus operator"""
import re
from itertools import chain

with open("day14.txt") as f_in:
    ins = [_.strip() for _ in f_in]


class Docking:
    MEM_RE = re.compile(r"mem\[(\d+)\] = (\d+)")

    def __init__(self, lines):
        self.lines, self.bitmask = lines, ""
        self.data = {}

    def sum(self, v2=False):
        for line in self.lines:
            if mem := self.MEM_RE.search(line):
                self.assignment(*mem.groups(), v2=v2)
            else:
                self.bitmask = line.strip("mask = ")
        return sum(self.data.values())

    def assignment(self, address, value, v2):
        def floating_addr(mask=None):
            if mask is None:
                mask = "".join(
                    a if m == '0' else '1' if m == '1' else 'X'
                    for a, m in zip(f'{address:036b}', self.bitmask)
                )
            if 'X' in mask:
                return chain(
                    floating_addr(mask.replace('X', '0', 1)),
                    floating_addr(mask.replace('X', '1', 1))
                )
            return [int(mask, 2)]

        address = int(address)
        value = int(value)
        if v2:
            for address in floating_addr():
                self.data[address] = value
        else:
            value |= int(self.bitmask.replace('X', '0'), 2)
            value &= int(self.bitmask.replace('X', '1'), 2)
            self.data[address] = value


docking = Docking(ins)
print(f"Result 1: {docking.sum()}")
docking.data = {}
print(f"Result 2: {docking.sum(True)}")
