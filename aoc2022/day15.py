from aoc.file import example, puzzle_input
from dataclasses import dataclass
from collections import namedtuple
from itertools import pairwise
from functools import cached_property
import math
from typing import Iterable, List, Mapping, Tuple
from tqdm import tqdm
import re

EX_TEXT = """\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""

SENSOR_RE = re.compile(r"x=(-*\d+), y=(-*\d+)")
Coord = Tuple[int, int]


def coord_sum(a: Coord, b: Coord) -> Coord:
    return a[0] + b[0], a[1] + b[1]


def axis_range(value: int, dist: int, local=None) -> Iterable[int]:
    if local is None:
        return range(-dist, dist + 1)
    elif -dist <= local - value <= dist:
        return [local - value]
    return []


def manhattan_range(
    visited: Mapping[Coord, str], a: Coord, dist: int, col=None, row=None
) -> Coord:
    for y in axis_range(a[1], dist, row):
        for x in axis_range(a[0], dist, col):
            b = coord_sum(a, (x, y))
            if b in visited:
                continue
            if abs(x) + abs(y) <= dist:
                yield b

@dataclass
class Sensor:
    loc: Coord
    beacon: Coord

    def __hash__(self):
        return hash(self.loc)

    @cached_property
    def beacon_dist(self) -> int:
        a, b = self.loc, self.beacon
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def update_view(self, view, col=None, row=None):
        for point in manhattan_range(
            view, self.loc, self.beacon_dist, col=col, row=row
        ):
            if point not in [self.loc, self.beacon]:
                view[point] = "#"
            elif point == self.loc:
                view[point] = "S"
            elif point == self.beacon:
                view[point] = "B"


def parser(lines):
    sensors = set()
    for line in lines:
        t1, t2 = SENSOR_RE.findall(line)
        sensor_loc = tuple(map(int, t1))
        beacon_loc = tuple(map(int, t2))
        sensors.add(Sensor(sensor_loc, beacon_loc))
    return sensors


def solver(lines, row):
    sensors = parser(lines)
    grid = {}
    for s in tqdm(sensors):
        s.update_view(grid, row=row)
    seen_on_row = len({p for p, v in grid.items() if v == "#"})
    return seen_on_row, None


print("Puzzle Example")
res1, res2 = solver(example(EX_TEXT), 10)
assert (res1, res2) == (26, None)
print("Puzzle Input")
res1, res2 = solver(puzzle_input(), 2000000)
print(f"Result 1: {res1}")
print(f"Result 2: {res2}")



