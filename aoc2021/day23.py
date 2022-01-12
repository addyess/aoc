from astar import AStar


def distance(a, b):
    return sum(abs(d1 - d2) for d1, d2 in zip(a, b))


class Amphipod:
    ENERGY = {
        "A": 1,
        "B": 10,
        "C": 100,
        "D": 1000,
    }

    def __init__(self, kind, start):
        self.pos = self.start = start
        self.kind = kind
        self.moves = 0
        self.shaft = (ord(self.kind) - ord("A")) * 2 + 2

    def __repr__(self):
        return f"{self.kind}@{self.pos}"

    def reset(self):
        self.pos = self.start
        self.moves = 0

    @property
    def score(self):
        return self.ENERGY[self.kind] * self.moves

    @property
    def optimal(self):
        return self.pos == (self.shaft, 2)

    def move(self, pos):
        self.moves += distance(self.pos, pos)
        self.pos = pos

    def distance(self, grid):
        if self.optimal:
            # Bottom of Shaft, don't move it
            return 0,
        x_dist = abs(self.shaft - self.pos[0])
        pair = [a for a in grid.amphipods if a != self and a.kind == self.kind][0]
        pair_is_fixed = pair.optimal
        y_dist = (1,) if pair_is_fixed else (1, 2)

        if self.pos[1] == 0:
            # in the hallway
            pass
        elif x_dist != 0:
            # wrong shaft
            y_dist = tuple(self.pos[1] + _ for _ in y_dist)
        elif self.pos[1] == 1 and pair_is_fixed:
            # Top of Shaft, above other of same type
            return 0,
        elif self.pos[1] == 1 and not pair_is_fixed:
            # Right Shaft, Wrong Spot
            return 1,
        return tuple(x_dist + _ for _ in y_dist)


class Nodes(AStar):
    def __init__(self, grid, amp_id: int):
        self.grid = grid
        self.this_amp = self.grid.amphipods[amp_id]

    def neighbors(self, node):
        tracks = {
            (0, 0): {(1, 0)},
            (1, 0): {(0, 0), (3, 0), (2, 1)},
            (3, 0): {(1, 0), (5, 0), (2, 1), (4, 1)},
            (5, 0): {(3, 0), (7, 0), (4, 1), (6, 1)},
            (7, 0): {(5, 0), (9, 0), (6, 1), (8, 1)},
            (9, 0): {(7, 0), (10, 0), (8, 1)},
            (10, 0): {(9, 0)},
            (2, 1): {(1, 0), (3, 0), (2, 2)},
            (4, 1): {(3, 0), (5, 0), (4, 2)},
            (6, 1): {(5, 0), (7, 0), (6, 2)},
            (8, 1): {(7, 0), (9, 0), (8, 2)},
            (2, 2): {(2, 1)},
            (4, 2): {(4, 1)},
            (6, 2): {(6, 1)},
            (8, 2): {(8, 1)},
        }
        locations = tracks[node]

        def safe(loc):
            occupied = {a.pos for a in self.grid.amphipods if a != self.this_amp}
            safer = loc - occupied
            return safer

        return safe(locations)

    def distance_between(self, n1, n2):
        _, ay = self.this_amp.pos
        dx, dy = n2
        if ay == 0 and dy != 0 and dx != self.this_amp.shaft:
            # amp is in the hallway, distance into wrong shaft are inf
            return float('inf')
        if ay == 0 and dx == self.this_amp.shaft:
            # amp is in the hallway, wanting to enter correct shaft
            # there can't be any wrong amps in this shaft
            bottom = next((a for a in self.grid.amphipods if a.pos == (dx, 2)), None)
            if bottom and bottom.kind != self.this_amp.kind:
                return float('inf')
        return distance(n1, n2)

    def heuristic_cost_estimate(self, current, goal):
        return distance(current, goal)


class Grid:
    def __init__(self, amphipods):
        self.amphipods = amphipods

    @classmethod
    def parse(cls, lines):
        y, amps = 1, []
        for line in lines:
            pos = [c for c in line if c in "ABCD"]
            amps += [Amphipod(c, (loc * 2 + 2, y)) for loc, c in enumerate(pos)]
            y += 1 if pos else 0
            if not line.strip():
                break
        return cls(amps)

    def score(self, path):
        for node, target in path:
            a = self.amphipods[node]
            p = Nodes(self, node).astar(a.pos, target)
            assert p
            for step in p:
                a.move(step)
        return sum(_.score for _ in self.amphipods)


def paths(g_input):
    return [eval(line) for line in g_input if not line.startswith('#')]


def solve(g_input):
    grid = Grid.parse(g_input)
    print(grid.score(paths(g_input)))


with open("day23.txt") as fin:
    solve(fin)
