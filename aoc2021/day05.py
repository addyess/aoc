from dataclasses import dataclass
from itertools import filterfalse, combinations, repeat
from functools import cached_property


@dataclass
class Line:
    start: tuple[int, int]
    end: tuple[int, int]

    @staticmethod
    def as_coord(xy_str):
        return tuple(map(int, xy_str.split(",")))

    @classmethod
    def parse(cls, lines):
        return [cls(*(cls.as_coord(_) for _ in line.split("->"))) for line in lines]

    @cached_property
    def diagonal(self):
        return self.start[0] != self.end[0] and self.start[1] != self.end[1]

    @cached_property
    def points(self):
        return set(zip(self.p_range(0), self.p_range(1)))

    def p_range(self, index):
        start, end = self.start[index], self.end[index]
        if start == end:
            return repeat(start)
        if max(start, end) == end:
            return range(start, end + 1)
        return reversed(range(end, start + 1))


def main():
    with open("day05.txt") as f_in:
        ins = [_.strip() for _ in f_in]
    lines = Line.parse(ins)
    non_diag = filterfalse(lambda l: l.diagonal, lines)
    intersections = (a.points & b.points for a, b in combinations(non_diag, 2))
    intersect_2_or_more = set(p for s in intersections for p in s)
    print(f"Result 1: {len(intersect_2_or_more)}")

    intersections = (a.points & b.points for a, b in combinations(lines, 2))
    intersect_2_or_more = set(p for s in intersections for p in s)
    print(f"Result 2: {len(intersect_2_or_more)}")


main()
