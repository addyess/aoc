from collections import defaultdict
import math


class Cave:
    def __init__(self, lines):
        self.map = {
            (x, y): int(height)
            for x, line in enumerate(lines)
            for y, height in enumerate(line.strip())
        }
        self.inf_boundary_map = defaultdict(lambda: float("inf"), self.map.items())
        self.low_points = {
            loc: height + 1
            for loc, height in self.map.items()
            if height < min(self.inf_boundary_map[a] for a in self.adjacent(loc))
        }

    @staticmethod
    def adjacent(pos):
        pos_x, pos_y = pos
        for x, y in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            yield pos_x + x, pos_y + y

    def adjacent_members_of_basin(self, loc, basin_set=None):
        basin_set = (basin_set or set()) | {loc}
        for a in self.adjacent(loc):
            if a not in basin_set and self.inf_boundary_map[a] < 9:
                basin_set |= self.adjacent_members_of_basin(a, basin_set)
        return basin_set

    @property
    def basins(self):
        return {lp: len(self.adjacent_members_of_basin(lp)) for lp in self.low_points}


with open("day09.txt") as fin:
    cave = Cave(fin)
res1 = sum(cave.low_points.values())
print(f"Result 1: {res1}")
largest_basins = sorted(cave.basins.values(), reverse=True)
res2 = math.prod(largest_basins[:3])
print(f"Result 2: {res2}")
