#! /usr/bin/python3
from aoc.file import example, puzzle_input

EX_TEXT = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""


def as_range_set(s_range):
    s, e = map(int, s_range.split("-"))
    return set(range(s, e + 1))


def solver(lines):
    full, partial = 0, 0
    for line in lines:
        e1, e2 = map(as_range_set, line.split(","))
        if e1.issubset(e2) or e2.issubset(e1):
            full += 1
        if not e1.isdisjoint(e2):
            partial += 1
    return full, partial


assert (2, 4) == solver(example(EX_TEXT))

res1, res2 = solver(puzzle_input())
print(f"Result 1 {res1}")
print(f"Result 2 {res2}")
