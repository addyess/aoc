from astar import AStar
from math import hypot


class Path(AStar):
    DIR = {
        "nw": (0, -1),
        "n": (1, -1),
        "ne": (1, 0),
        "se": (0, 1),
        "s": (-1, 1),
        "sw": (-1, 0),
    }

    def neighbors(self, node):
        for offset in self.DIR.values():
            yield tuple(map(sum, zip(node, offset)))

    def distance_between(self, n1, n2):
        return 1

    def heuristic_cost_estimate(self, current, goal):
        x, y = tuple(map(lambda t: abs(t[0] - t[1]), zip(current, goal)))
        return hypot(x, y)

    def __init__(self, steps):
        self.nodes = []
        self.start = pos = (0, 0)
        for step in steps.split(","):
            offset = Path.DIR[step]
            pos = tuple(map(sum, zip(pos, offset)))
            self.nodes.append(pos)
        self.goal = pos

    def steps(self):
        return len(list(self.astar(self.start, self.goal))) - 1

    def furthest(self):
        # heuristic distance from start to each node
        distances = {
            node: self.heuristic_cost_estimate(self.start, node) for node in self.nodes
        }
        # take 250 of the furthest heuristic distances
        by_dist = dict(
            sorted(distances.items(), key=lambda t: t[1], reverse=True)[:250]
        )
        # find the paths to those 250 nodes, and find the furthest ones
        paths = sorted(
            [len(list(self.astar(self.start, node))) for node in by_dist.keys()]
        )
        return paths[-1] - 1


assert Path("ne,ne,ne").steps() == 3
assert Path("ne,ne,sw,sw").steps() == 0
assert Path("nw,ne").steps() == 1
assert Path("ne,ne,s,s").steps() == 2
assert Path("se,sw,se,sw,sw").steps() == 3
assert Path("se,sw,se,sw,sw").furthest() == 3

with open("day11.txt") as fin:
    path = Path(fin.read())

print(f"Result 1: {path.steps()}")
print(f"Result 2: {path.furthest()}")
# 1411 too low
# 1419 too low
