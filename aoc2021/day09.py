from collections import defaultdict
from dataclasses import dataclass
from functools import cached_property
import math


@dataclass
class Cave:
    height_map: dict[tuple, int]

    @classmethod
    def parse(cls, lines):
        return cls(
            {
                (x, y): int(height)
                for x, line in enumerate(lines)
                for y, height in enumerate(line.strip())
            }
        )

    @staticmethod
    def adjacent(pos):
        pos_x, pos_y = pos
        for x, y in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            yield pos_x + x, pos_y + y

    @cached_property
    def inf_boundary_map(self):
        return defaultdict(lambda: float("inf"), self.height_map.items())

    @cached_property
    def low_points(self):
        """Finds the lowest local points, and returns the score at those points."""
        return {
            loc: height + 1
            for loc, height in self.height_map.items()
            if height < min(self.inf_boundary_map[a] for a in self.adjacent(loc))
        }

    @cached_property
    def basins(self):
        """
        Finds each basin lower than height 9 centered on their low-point, and provides
        the coordinates to each point in the basin
        """

        def adjacent_members_of_basin(loc, basin_set=None):
            basin_set = (basin_set or set()) | {loc}
            for a in self.adjacent(loc):
                if a not in basin_set and self.inf_boundary_map[a] < 9:
                    basin_set |= adjacent_members_of_basin(a, basin_set)
            return basin_set

        return {lp: len(adjacent_members_of_basin(lp)) for lp in self.low_points}


with open("day09.txt") as fin:
    cave = Cave.parse(fin)
res1 = sum(cave.low_points.values())
print(f"Result 1: {res1}")
largest_basins = sorted(cave.basins.values(), reverse=True)
res2 = math.prod(largest_basins[:3])
print(f"Result 2: {res2}")
