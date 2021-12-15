from dijkstra import Graph, DijkstraSPF
from math import sqrt


class Cave:
    def __init__(self, lines):
        self.risks = {
            (x, y): int(risk)
            for y, line in enumerate(lines)
            for x, risk in enumerate(line.strip())
        }
        self.dim = int(sqrt(len(self.risks)))

    def new_risk(self, exist_loc, new_loc):
        new_risk = self.risks[exist_loc] + 1
        new_risk = 1 if new_risk > 9 else new_risk
        self.risks[new_loc] = new_risk

    def expand(self, size=5):
        existing = dict(self.risks.items())
        self.dim, dim = self.dim * size, self.dim
        for my in range(size - 1):
            for mx in range(size - 1):
                for x, y in existing.keys():
                    exist_loc = mx * dim + x, my * dim + y
                    down_loc = mx * dim + x, (my + 1) * dim + y
                    right_loc = (mx + 1) * dim + x, my * dim + y
                    middle_loc = (mx + 1) * dim + x, (my + 1) * dim + y
                    self.new_risk(exist_loc, down_loc)
                    self.new_risk(exist_loc, right_loc)
                    self.new_risk(right_loc, middle_loc)

    def neighbors(self, node):
        for offset in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            new = tuple(map(sum, zip(node, offset)))
            if new in self.risks:
                yield new

    @property
    def total_risk(self):
        graph = Graph()
        for k in self.risks.keys():
            for n in self.neighbors(k):
                graph.add_edge(k, n, self.risks[n])
        start, goal = (0, 0), (self.dim - 1, self.dim - 1)
        d = DijkstraSPF(graph, start)
        return sum(self.risks[n] for n in d.get_path(goal) if n != start)


with open("day15.txt") as fin:
    cave = Cave(fin)
print(f"Result 1: {cave.total_risk}")
cave.expand()
print(f"Result 2: {cave.total_risk}")
