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

    def __init__(self, kind, start, moves=0):
        self.pos = self.start = start
        self.kind = kind
        self.moves = moves
        self.room = (ord(self.kind) - ord("A")) * 2 + 2

    def __repr__(self):
        return f"{self.kind}@{self.pos}"

    def at_home(self, grid):
        """If I am in the right room, and all other amps deeper in this room are the same kind."""
        x, y = self.pos
        return self.room == x and all(
            a.kind == self.kind
            for a in grid.amphipods
            if x == a.pos[0] and y < a.pos[1]
        )

    @property
    def score(self):
        return self.ENERGY[self.kind] * self.moves

    def move(self, steps):
        for pos in steps:
            self.moves += distance(self.pos, pos)
            self.pos = pos

    def home(self, grid):
        roommates = {a for a in grid.amphipods if a.pos[0] == self.room}
        if all(r.kind == self.kind for r in roommates):
            return [(self.room, grid.depth - len(roommates))]
        return []


class Nodes(AStar):
    TRACKS = {
        (0, 0): {(1, 0)},
        (1, 0): {(0, 0), (3, 0), (2, 1)},
        (3, 0): {(1, 0), (5, 0), (2, 1), (4, 1)},
        (5, 0): {(3, 0), (7, 0), (4, 1), (6, 1)},
        (7, 0): {(5, 0), (9, 0), (6, 1), (8, 1)},
        (9, 0): {(7, 0), (10, 0), (8, 1)},
        (10, 0): {(9, 0)},
        (2, 1): {(1, 0), (3, 0), (2, 2)},
        (2, 2): {(2, 1), (2, 3)},
        (2, 3): {(2, 2), (2, 4)},
        (2, 4): {(2, 3)},
        (4, 1): {(3, 0), (5, 0), (4, 2)},
        (4, 2): {(4, 1), (4, 3)},
        (4, 3): {(4, 2), (4, 4)},
        (4, 4): {(4, 3)},
        (6, 1): {(5, 0), (7, 0), (6, 2)},
        (6, 2): {(6, 1), (6, 3)},
        (6, 3): {(6, 2), (6, 4)},
        (6, 4): {(6, 3)},
        (8, 1): {(7, 0), (9, 0), (8, 2)},
        (8, 2): {(8, 1), (8, 3)},
        (8, 3): {(8, 2), (8, 4)},
        (8, 4): {(8, 3)},
    }

    def __init__(self, grid, amp_id: int):
        self.grid = grid
        self.this_amp = self.grid.amphipods[amp_id]

    def neighbors(self, node):
        occupied = {a.pos for a in self.grid.amphipods if a != self.this_amp}
        safer = {pos for pos in self.TRACKS[node] if pos[1] <= self.grid.depth} - occupied
        return safer

    def distance_between(self, n1, n2):
        kind, room = self.this_amp.kind, self.this_amp.room
        _, ay = n1
        dx, dy = n2
        if ay == 0 and dy != 0 and dx != room:
            # amp cannot enter the wrong rooms
            return float("inf")
        if ay == 0 and dx == room:
            # amp wants to enter correct room
            # there can't be any wrong amps in this room
            if any(a for a in self.grid.amphipods if a.pos[0] == dx and a.kind != kind):
                return float("inf")
        return distance(n1, n2)

    def heuristic_cost_estimate(self, current, goal):
        return distance(current, goal)

    def steps(self, target):
        return self.astar(self.this_amp.pos, target)


class Grid:
    def __init__(self, amphipods, depth):
        self.amphipods = amphipods
        self.depth = depth

    @classmethod
    def parse(cls, lines, depth=2):
        y, amps = 1, []
        for line in lines:
            pos = [c for c in line if c in "ABCD"]
            amps += [Amphipod(c, (loc * 2 + 2, y)) for loc, c in enumerate(pos)]
            y += 1 if pos else 0
            if not line.strip():
                break
        return cls(amps, depth)

    def copy(self):
        copy = [Amphipod(a.kind, a.pos, a.moves) for a in self.amphipods]
        return Grid(copy, self.depth)

    def unfold(self):
        grid = self.copy()
        grid.depth = 4
        unfolded = [(2, "DCBA"), (3, "DBAC")]
        amps = [
            Amphipod(c, (loc * 2 + 2, y))
            for y, line in unfolded
            for loc, c in enumerate(line)
        ]
        for a in reversed(amps):
            grid.amphipods.insert(4, a)
        for a in grid.amphipods[12:]:
            x, y = a.pos
            a.pos = x, y + 2
        return grid

    @property
    def score(self):
        return sum(_.score for _ in self.amphipods)

    @property
    def is_solved(self):
        return all(a.pos[0] == a.room for a in self.amphipods)

    @property
    def available_moves(self):
        for amp_id, amp in sorted(enumerate(self.amphipods), key=lambda a: a[1].kind):
            if amp.at_home(self):
                continue
            homes = amp.home(self)
            positions = {pos for pos in Nodes.TRACKS.keys() if pos[1] <= self.depth}
            occupied = {a.pos for a in self.amphipods if a.pos != amp.pos}
            empties = positions - occupied
            if amp.pos[1] == 0:
                # if amp is in hallway, it can ONLY go into its home
                empties &= set(homes)
            else:
                # if amp is in a room, it can ONLY go into hallway or its home
                empties = {pos for pos in empties if pos[1] == 0 or pos in homes}
            for empty in sorted(empties, key=lambda p: distance(amp.pos, p)):
                yield amp_id, empty

    def solve(self, path, low_score=float("inf")):
        """
        Returns None if the grid is unsolvable or produces only higher scores from this point on.
        Returns new low winning score and path taken to arrive at it
        """
        if self.is_solved:
            if self.score < low_score:
                print(f"{self.depth}: {self.score} ({path[:3]}...)")
                return self.score, path
            return None
        if self.score >= low_score:
            return None
        lowest_path = None
        for amp_id, target in self.available_moves:
            steps = Nodes(self, amp_id).steps(target)
            if not steps:
                continue
            grid = self.copy()
            grid.amphipods[amp_id].move(steps)
            result = grid.solve(path + [(amp_id, target)], low_score)
            if result is None:
                continue
            low_score, lowest_path = result
        if lowest_path:
            return low_score, lowest_path


def solve(g_input):
    part1 = Grid.parse(g_input)
    part2 = part1.unfold()
    score, path = part1.solve([])
    print(f"Result #1: {score}")
    score, path = part2.solve([])
    print(f"Result #2: {score}")


with open("day23.txt") as fin:
    print("This will take hours -- run and wait.")
    solve(fin)
