#! /usr/bin/python3
from aoc.file import puzzle_input, example
from enum import Enum
from dataclasses import dataclass


EX_TEXT = """30373
25512
65332
33549
35390"""


Direction = Enum("Direction", ["LEFT", "RIGHT", "UP", "DOWN"], start=0)


def mul(iterable):
    prod = 1
    for v in iterable:
        prod = v * prod if prod else 0
    return prod


@dataclass
class Grove:
    h: int
    w: int
    data: dict

    def _visible(self, x, y):
        me = self.data[(x, y)]
        return (
            all(me > self.data[(_, y)] for _ in range(0, x))
            or all(me > self.data[(_, y)] for _ in range(x + 1, self.w))
            or all(me > self.data[(x, _)] for _ in range(0, y))
            or all(me > self.data[(x, _)] for _ in range(y + 1, self.h))
        )

    def _dist(self, x, y, direction: Direction):
        me, dir = self.data[(x, y)], direction.value
        ranges = [
            (x - 1, -1, -1),  # LEFT of x,y
            (x + 1, self.w, 1),  # RIGHT of x,y
            (y - 1, -1, -1),  # UP above x,y
            (y + 1, self.h, 1),  # DOWN below x,y
        ][dir]
        compare = [
            lambda c: self.data[(c, y)] >= me,
            lambda c: self.data[(c, y)] >= me,
            lambda c: self.data[(x, c)] >= me,
            lambda c: self.data[(x, c)] >= me,
        ][dir]
        axis_dist = [
            lambda c: abs(x - c),
            lambda c: abs(x - c),
            lambda c: abs(y - c),
            lambda c: abs(y - c),
        ][dir]
        for _ in range(*ranges):
            if compare(_):
                return axis_dist(_)
        return abs(ranges[1] - ranges[0])

    def visibility(self):
        return [self._visible(x, y) for x in range(0, self.w) for y in range(0, self.h)]

    def scenic_score(self):
        return [
            mul(self._dist(x, y, d) for d in Direction)
            for x in range(0, self.w)
            for y in range(0, self.h)
        ]


def parse_trees(lines):
    grove = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            grove[(x, y)] = int(c)
    return Grove(y + 1, x + 1, grove)


def solver(lines):
    grove = parse_trees(lines)
    return sum(grove.visibility()), max(grove.scenic_score())


res1, res2 = solver(example(EX_TEXT))
assert (res1, res2) == (21, 8)
res1, res2 = solver(puzzle_input())
print(f"Result 1: {res1}")
print(f"Result 2: {res2}")
