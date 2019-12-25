from itertools import count, chain, takewhile


class Eris:
    DIRS = {(0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)}

    @classmethod
    def parse(cls, lines, recursive=None):
        return cls({
            (x, y, 0): c
            for y, line in enumerate(lines)
            for x, c in enumerate(line)
        }, recursive)

    def __init__(self, grid, recursive):
        self.grid = grid
        self.recursive = recursive
        if recursive:
            self.grid.pop((2, 2, 0), None)

    def __iter__(self):
        return self

    @staticmethod
    def sum(a, b):
        return tuple(sum(_) for _ in zip(a, b))

    def at(self, a):
        return self.grid.get(a) or '.'

    def adjacent(self, a):
        x, y, z = a
        base = set(self.sum(a, _) for _ in self.DIRS)
        if not self.recursive:
            return base
        if x == 0:
            base = (base - {(x - 1, y, z)}) | {(1, 2, z - 1)}
        elif x == 4:
            base = (base - {(x + 1, y, z)}) | {(3, 2, z - 1)}
        if y == 0:
            base = (base - {(x, y - 1, z)}) | {(2, 1, z - 1)}
        elif y == 4:
            base = (base - {(x, y + 1, z)}) | {(2, 3, z - 1)}

        if (x, y) == (2, 1):
            base = (base - {(x, y + 1, z)}) | {(_, 0, z + 1) for _ in range(5)}
        elif (x, y) == (2, 3):
            base = (base - {(x, y - 1, z)}) | {(_, 4, z + 1) for _ in range(5)}
        elif (x, y) == (1, 2):
            base = (base - {(x + 1, y, z)}) | {(0, _, z + 1) for _ in range(5)}
        elif (x, y) == (3, 2):
            base = (base - {(x - 1, y, z)}) | {(4, _, z + 1) for _ in range(5)}
        return base

    def bugs(self, a):
        vals = [self.at(_) for _ in self.adjacent(a)]
        return sum(1 if _ == '#' else 0 for _ in vals)

    def next(self, a):
        is_bug, bug_c = self.at(a) == '#', self.bugs(a)
        if (is_bug and bug_c == 1) or (not is_bug and bug_c in [1, 2]):
            return "#"
        return "."

    def domain(self):
        base = sorted(self.grid.keys())
        if not self.recursive:
            return base
        _, expand = self.recursive
        self.recursive = _, not expand
        additional = set()
        if expand:
            x, y, z = zip(*self.grid.keys())
            minz, maxz = min(z), max(z)

            additional = list(
                (x, y, z)
                for z in [minz-1, maxz+1]
                for y in range(5)
                for x in range(5)
                if (x, y) != (2, 2)
            )
        return chain(base, additional)

    def __next__(self):
        ngrid = {_: self.next(_) for _ in self.domain()}
        eris = Eris(ngrid, self.recursive)
        return eris

    def __eq__(self, other):
        return self.grid == other

    def rating(self):
        x, y, z = zip(*self.grid.keys())
        bugs = [self.at((x1, y1, z1)) == '#' for y1 in range(max(y) + 1) for x1 in range(max(x) + 1) for z1 in
                range(max(z) + 1)]
        pows = [2 ** _ for _ in range(len(self.grid.keys()))]
        return sum(c for b, c in zip(bugs, pows) if b)

    def print(self, *args):
        if len(args) == 0:
            x, y, z = zip(*self.grid.keys())
            minz, maxz = min(z), max(z)
            for z in range(minz, maxz + 1):
                self.print(x, y, z)
            return

        x, y, z = args
        print(f"Depth {z}:")
        for y1 in range(max(y) + 1):
            print("".join(self.grid.get((_, y1, z)) or '?' for _ in range(max(x) + 1)))
        print()


def main():
    with open("day24.txt") as fin:
        ins = fin.read()

    history = list()
    eris = Eris.parse(ins.strip().splitlines())
    for _ in count():
        if any(_ == eris for _ in history):
            break
        history.append(eris)
        eris = next(eris)
    print(f"Result 1: {eris.rating()}")

    eris = Eris.parse(ins.strip().splitlines(), (True, True))
    for i in range(0, 200):
        eris = next(eris)
    eris.print()
    print(f"Result 2: {len([_ for _ in eris.grid.values() if _ == '#'])}")

main()
