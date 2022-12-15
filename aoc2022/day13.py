#! /usr/bin/python3
from aoc.file import example, puzzle_input
from dataclasses import dataclass
from enum import Enum
from functools import cache
from itertools import zip_longest
import math
from typing import List, Iterable

EX_TEXT = """\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""

Cmp = Enum("Cmp", ("LT", "GT", "EQ"))
DIV = """[[2]]\n[[6]]"""


@dataclass
class Packet:
    data: List
    marked: bool = False

    @classmethod
    def inner_cmp(cls, left, right):
        if left is None:
            return Cmp.LT
        if right is None:
            return Cmp.GT
        if isinstance(left, int) and isinstance(right, int):
            if left == right:
                return Cmp.EQ
            elif left < right:
                return Cmp.LT
            return Cmp.GT
        if isinstance(left, int) and isinstance(right, list):
            left = cls([left])
            right = cls(right)
        elif isinstance(left, list) and isinstance(right, int):
            left = cls(left)
            right = cls([right])
        elif isinstance(left, list) and isinstance(right, list):
            left = cls(left)
            right = cls(right)

        if left == right:
            return Cmp.EQ
        elif left < right:
            return Cmp.LT
        return Cmp.GT

    def _comparison(self, other: "Packet") -> Iterable[bool]:
        return (self.inner_cmp(*pair) for pair in zip_longest(self.data, other.data))

    def __lt__(self, other: "Packet") -> bool:
        if self == other:
            return False
        for c in self._comparison(other):
            if c == Cmp.EQ:
                continue
            return c == Cmp.LT
        raise TypeError(f"'<' not supported between {self} and {other}")

    def __eq__(self, other: "Packet") -> bool:
        return all(c == Cmp.EQ for c in self._comparison(other))


def parser(lines, mark=False):
    while True:
        try:
            pair = Packet(eval(next(lines)), mark), Packet(eval(next(lines)), mark)
            yield pair
            next(lines)
        except StopIteration:
            return


def solver(lines):
    pairs = list(parser(lines))
    calc = [left < right for left, right in pairs]
    p1 = sum(idx + 1 for idx, lt in enumerate(calc) if lt)

    pairs += list(parser(iter(DIV.splitlines()), mark=True))
    sorted_packets = sorted(p for pair in pairs for p in pair)
    p2 = math.prod(idx + 1 for idx, p in enumerate(sorted_packets) if p.marked)
    return p1, p2


print("Puzzle Example")
res1, res2 = solver(example(EX_TEXT))
assert (res1, res2) == (13, 140)
print("Puzzle Input")
res1, res2 = solver(puzzle_input())
print(f"Result 1: {res1}")
print(f"Result 2: {res2}")
