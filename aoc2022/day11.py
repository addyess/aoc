#! /usr/bin/python3
from aoc.file import puzzle_input
from dataclasses import dataclass, asdict
from typing import List, Iterable, Tuple
import math
from operator import mul, add
import re

INTS_RE = re.compile(r"(\d+)(?:, ){0,1}")
OPS_RE = re.compile(r"Operation: new = old (\S) (\S+)")
OPS = {"*": mul, "+": add}


@dataclass
class Monkey:
    key: int
    items: List[int]
    operation: Tuple[str, str]
    divisible_by: int
    true_monkey: int
    fail_monkey: int
    fear_mul: int = 3
    lcm: int = 0
    inspections: int = 0

    def __repr__(self):
        return str(self.inspections)

    @classmethod
    def multi_parse(cls, lines: Iterable[str]) -> Iterable["Monkey"]:
        while True:
            yield cls.parse(lines)
            try:
                next(lines)
            except StopIteration:
                return

    @classmethod
    def parse(cls, lines: Iterable[str]) -> "Monkey":
        (key_id,) = map(int, INTS_RE.findall(next(lines)))
        (*starting,) = map(int, INTS_RE.findall(next(lines)))
        (ops,) = OPS_RE.findall(next(lines))
        (div,) = map(int, INTS_RE.findall(next(lines)))
        (truth,) = map(int, INTS_RE.findall(next(lines)))
        (fail,) = map(int, INTS_RE.findall(next(lines)))
        return cls(key_id, starting, ops, div, truth, fail)

    def inspect(self, monkeys):
        op, value = self.operation
        for item in self.items:
            self.inspections += 1
            if value == "old":
                new = OPS[op](item, item)
            else:
                new = OPS[op](item, int(value))
            if self.fear_mul:
                new = new // self.fear_mul
            elif self.lcm:
                new = new % self.lcm
            if (new % self.divisible_by) == 0:
                target = self.true_monkey
            else:
                target = self.fail_monkey
            monkeys[target].items.append(new)
        self.items = []


def business(monkeys, rounds):
    for round in range(rounds):
        for monkey in monkeys.values():
            monkey.inspect(monkeys)
    a, b, *_ = sorted((m.inspections for m in monkeys.values()), reverse=True)
    return a * b


def solver(lines):
    m1 = {m.key: m for m in Monkey.multi_parse(lines)}
    lcm = math.prod(m.divisible_by for m in m1.values())
    m2 = {m.key: Monkey(**asdict(m) | {"fear_mul": 0, "lcm": lcm}) for m in m1.values()}
    e = business(m1, 20)
    f = business(m2, 10000)
    return e, f


res1, res2 = solver(puzzle_input("day11_ex.txt"))
assert (res1, res2) == (10605, 2713310158)
res1, res2 = solver(puzzle_input())
print(f"Result 1: {res1}")
print(f"Result 2: {res2}")
