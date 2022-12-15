#! /usr/bin/python3
from aoc.file import puzzle_input
from dataclasses import dataclass

CYCLES_PER = {
    "addx": 2,
    "noop": 1,
}

SAMPLE = """\
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....
"""
CRT = None


@dataclass
class Ins:
    name: str
    value: int


def parse_assm(lines):
    for line in lines:
        if line == "noop":
            yield Ins(line, 0)
        else:
            args = line.split()
            yield Ins(args[0], int(args[1]))


def execute(code):
    global CRT
    x, cycles, CRT = 1, 0, ""
    for ins in code:
        for tick in range(CYCLES_PER[ins.name]):
            cycles += 1
            crt_pos = (cycles - 1) % 40
            CRT += "#" if crt_pos in (x - 1, x, x + 1) else "."
            if crt_pos == 39:
                CRT += "\n"
            if cycles % 40 == 20:
                yield cycles * x
        x += ins.value


def solver(lines):
    analysis = sum(execute(parse_assm(lines)))
    return analysis, CRT


res1, res2 = solver(puzzle_input("day10_ex.txt"))
assert (res1, res2) == (13140, SAMPLE)
res1, res2 = solver(puzzle_input())
print(f"Result 1: {res1}")
print(f"Result 2: \n\n{res2}")
