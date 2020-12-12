from itertools import dropwhile

with open("day11.txt") as f_in:
    ins = [_.strip() for _ in f_in]


class Grid:
    @classmethod
    def parse(cls, text):
        return cls({
            (x, y): pos
            for y, line in enumerate(text)
            for x, pos in enumerate(line)
        })

    def __str__(self):
        maxx, maxy = max(self.data.keys())
        return "\n".join(
            "".join(self.data.get((x, y)) for x in range(0, maxx + 1))
            for y in range(0, maxy + 1)
        ) + "\n"

    def __init__(self, data):
        self.data = data

    def adjacent(self, x, y):
        vision = (
            self.data.get((x + dx, y + dy))
            for dx in range(-1, 2)
            for dy in range(-1, 2)
            if (dx, dy) != (0, 0)
        )
        return filter(None, vision)

    def in_sight(self, x, y):
        distance = max(max(self.data.keys()))
        vision = (
            next(dropwhile(
                lambda v: v == '.', (
                    self.data.get((x + dx * v, y + dy * v))
                    for v in range(1, distance + 1)
                )
            ))
            for dy in range(-1, 2)
            for dx in range(-1, 2)
            if (dx, dy) != (0, 0)
        )
        return filter(None, vision)

    def taken(self, x, y, adj_method, tolerance):
        adjacent = getattr(self, adj_method)
        taken = [_ == '#' for _ in adjacent(x, y)]
        return not any(taken), sum(taken) >= tolerance

    def step(self, adj_method, tolerance):
        new = {}
        maxx, maxy = max(self.data.keys())
        for y in range(0, maxy + 1):
            for x in range(0, maxx + 1):
                here = self.data.get((x, y))
                if here == '.':
                    new[(x, y)] = "."
                    continue
                none_taken, neighborly = self.taken(x, y, adj_method, tolerance)
                if here == 'L' and none_taken:
                    new[(x, y)] = "#"
                    continue
                if here == '#' and neighborly:
                    new[(x, y)] = "L"
                    continue
                new[(x, y)] = here
        return Grid(new)

    @property
    def occupied(self):
        return len([_ for _ in self.data.values() if _ == "#"])

    @staticmethod
    def run(_grid, *args):
        while True:
            grid_1 = _grid.step(*args)
            if grid_1.data == _grid.data:
                break
            _grid = grid_1
        return _grid.occupied


grid = Grid.parse(ins)
print(f"Result 1: {grid.run(grid, 'adjacent', 4)}")
print(f"Result 2: {grid.run(grid, 'in_sight', 5)}")
