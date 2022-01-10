import re
from collections import namedtuple
from functools import cached_property


def range_inc(md, Md):
    return range(md, Md + 1)


def range_diff(dim):
    return max(dim) - min(dim) + 1


def range_split(a, b):
    (ma, Ma), (mb, Mb) = a, b
    assert ma <= mb <= Mb <= Ma
    return (
        (ma, mb - 1) if mb != ma else None,
        (mb, Mb),
        (Mb + 1, Ma) if Ma != Mb else None,
    )


def range_reduce(dim, max_size):
    min_size = max_size * -1
    left, right = dim
    left, right = max(left, min_size), min(right, max_size)
    return (left, right) if left <= right else None


class Cuboid(namedtuple("Cuboid", "state, x, y, z")):
    step_re = re.compile(
        r"(?P<state>on|off) x=(?P<x1>-?\d+)..(?P<x2>-?\d+),y=(?P<y1>-?\d+)..(?P<y2>-?\d+),z=(?P<z1>-?\d+)..(?P<z2>-?\d+)"
    )

    @classmethod
    def parse(cls, lines):
        gen = (cls.step_re.match(line) for line in lines)
        return [
            cls(
                m.group("state") == "on",
                tuple(map(int, (m.group(_) for _ in ["x1", "x2"]))),
                tuple(map(int, (m.group(_) for _ in ["y1", "y2"]))),
                tuple(map(int, (m.group(_) for _ in ["z1", "z2"]))),
            )
            for m in gen
            if m
        ]

    @cached_property
    def init_dims(self):
        return tuple(range_reduce(_, 50) for _ in (self.x, self.y, self.z))

    @cached_property
    def size(self):
        return range_diff(self.x) * range_diff(self.y) * range_diff(self.z)

    def __and__(self, other):
        """Finds cuboid where self and other overlap. (set union operator &)"""
        o_x = self.dim_overlap(self.x, other.x)
        o_y = self.dim_overlap(self.y, other.y)
        o_z = self.dim_overlap(self.z, other.z)
        if all([o_x, o_y, o_z]):
            return Cuboid(True, o_x, o_y, o_z)

    def __sub__(self, other):
        if other is None:
            return set()
        return set(
            Cuboid(self.state, x, y, z)
            for z_id, z in enumerate(range_split(self.z, other.z))
            for y_id, y in enumerate(range_split(self.y, other.y))
            for x_id, x in enumerate(range_split(self.x, other.x))
            if not all(_ == 1 for _ in [x_id, y_id, z_id])
            if all([x, y, z])
        )

    @staticmethod
    def dim_overlap(self_dim, other_dim) -> tuple[int, int]:
        (ms, Ms), (mo, Mo) = self_dim, other_dim
        if any(
            (
                (ms <= mo <= Ms <= Mo),
                (ms <= mo <= Mo <= Ms),
                (mo <= ms <= Ms <= Mo),
                (mo <= ms <= Mo <= Ms),
            )
        ):
            return max(ms, mo), min(Ms, Mo)


class Ranges:
    def __init__(self):
        self.on_ranges = set()  # set of non-overlapping cuboids

    @property
    def initialized(self):
        r = Ranges()
        r.on_ranges = {
            Cuboid(True, *cube.init_dims)
            for cube in self.on_ranges
            if all(cube.init_dims)
        }
        return r

    @property
    def size(self):
        return sum(_.size for _ in self.on_ranges)

    def __ior__(self, other):
        """
        for when 'other' adds to the current cubes.
        de-dup and ranges in current on, and add other to the list
        """
        ranges = {other}
        for cube in self.on_ranges:
            overlap = cube & other
            if overlap:
                ranges |= cube - overlap
            else:
                ranges.add(cube)

        self.on_ranges = ranges
        return self

    def __sub__(self, other):
        """for when 'other' removes itself from the current cubes."""
        ranges = set()
        for cube in self.on_ranges:
            overlap = cube & other
            if not overlap:
                ranges.add(cube)
            else:
                ranges |= cube - overlap

        self.on_ranges = ranges
        return self


with open("day22.txt") as fin:
    cuboids = Cuboid.parse(fin)

cubes_on = Ranges()
for cuboid in cuboids:
    if cuboid.state:
        cubes_on |= cuboid
    else:
        cubes_on -= cuboid
print(f"Result #1: {cubes_on.initialized.size}")
print(f"Result #2: {cubes_on.size}")
