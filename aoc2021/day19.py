import re
from collections import namedtuple, defaultdict
from itertools import permutations, combinations


def rotations():
    for axis in permutations("xyz", 3):
        for x in [1, -1]:
            for y in [1, -1]:
                for z in [1, -1]:
                    yield Rotation("".join(axis), (x, y, z))


Alignment = namedtuple("Alignment", "source, target, offset")
Rotation = namedtuple("Rotation", "axis, dir")


class Coordinate(namedtuple("Coordinate", "x,y,z")):
    @classmethod
    def parse(cls, line):
        return cls(*eval(f"({line.strip()})"))

    def align(self, rot: Rotation):
        t = tuple((getattr(self, axis) for axis in rot.axis))
        return Coordinate(*(v * m for v, m in zip(t, rot.dir)))

    def __sub__(self, other):
        return Coordinate(*tuple(a - b for a, b in zip(self, other)))

    def __add__(self, other):
        return Coordinate(*tuple(a + b for a, b in zip(self, other)))

    def distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)


class Scanner:
    ID_RE = re.compile(r"--- scanner (\d+) ---")

    @classmethod
    def parse(cls, stream):
        all_scanners = []
        for line in stream:
            if not line.strip():
                continue
            id_line = cls.ID_RE.match(line)
            if id_line:
                all_scanners.append(cls(id_line.groups()[0]))
                continue
            all_scanners[-1].coordinates.add(Coordinate.parse(line))
        return all_scanners

    def __init__(self, _id):
        self.id = _id
        self.rotation = Rotation("xyz", (1, 1, 1))
        self.coordinates = set()
        self.scanners = set()

    def rotate(self, rot):
        scanner = Scanner(self.id)
        scanner.rotation = rot
        for c in self.coordinates:
            scanner.coordinates.add(c.align(rot))
        return scanner

    def aligns(self, other, rot):
        other = other.rotate(rot)
        diffs = defaultdict(set)
        for c1 in self.coordinates:
            for c2 in other.coordinates:
                o = c1 - c2
                diffs[o].add(c2)
                if len(diffs[o]) == 12:
                    return Alignment(self, other, o)

    def find_alignment(self, other):
        for rot in rotations():
            alignment = self.aligns(other, rot)
            if alignment:
                return alignment

    def map(self, others):
        alignments = {}
        incomplete = {s.id: s for s in others}
        next_sources = {others[0]}
        while incomplete:
            sources, next_sources = next_sources, set()
            for source in sources:
                if source.id in incomplete:
                    del incomplete[source.id]
                    gen = (source.find_alignment(s) for s in incomplete.values())
                    alignments[source.id] = [a for a in gen if a]
                    next_sources |= {a.target for a in alignments[source.id]}
        return self.join(alignments, "0", Coordinate(0, 0, 0))

    def join(self, alignments, s_id, offset):
        self.scanners.add(offset)
        for idx, alignment in enumerate(alignments[s_id]):
            if idx == 0:
                self.coordinates |= {c + offset for c in alignment.source.coordinates}
            self.coordinates |= {
                c + offset + alignment.offset for c in alignment.target.coordinates
            }
            self.join(alignments, alignment.target.id, offset + alignment.offset)
        return self

    def largest_manhattan(self):
        return max(a.distance(b) for a, b in combinations(self.scanners, 2))


with open("day19.txt") as fin:
    scanners = Scanner.parse(fin)
full_map = Scanner("full").map(scanners)
print(f"Result 1: {len(full_map.coordinates)}")
print(f"Result 2: {full_map.largest_manhattan()}")
