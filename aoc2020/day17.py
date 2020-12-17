from collections import defaultdict

with open("day17.txt") as f_in:
    ins = [_.strip() for _ in f_in]


class Conway4D:
    @classmethod
    def parse(cls, initial, n_dim):
        return cls(defaultdict(bool, (
            ((x, y, 0, 0), True)
            for y, line in enumerate(initial)
            for x, val in enumerate(line)
            if val == "#"
        )), n_dim)

    def neighbors(self, pos):
        x, y, z, w = pos
        ws = range(w - 1, w + 2) if self.n_dim == 4 else (0,)

        return set(
            (x1, y1, z1, w1)
            for x1 in range(x - 1, x + 2)
            for y1 in range(y - 1, y + 2)
            for z1 in range(z - 1, z + 2)
            for w1 in ws
        ) - {pos}

    def bounds(self):
        min_x, min_y, min_z, min_w = tuple(map(min, zip(*self.data.keys())))
        max_x, max_y, max_z, max_w = tuple(map(max, zip(*self.data.keys())))
        ws = range(min_w - 1, max_w + 2) if self.n_dim == 4 else (0,)

        return (
            (x, y, z, w)
            for x in range(min_x - 1, max_x + 2)
            for y in range(min_y - 1, max_y + 2)
            for z in range(min_z - 1, max_z + 2)
            for w in ws
        )

    def iterate(self, cycles):
        gen = self
        for _ in range(cycles):
            step = defaultdict(bool)
            for pos in gen.bounds():
                active, count = gen.data[pos], sum(
                    gen.data[neigh]
                    for neigh in gen.neighbors(pos)
                )
                if active and count in [2, 3]:
                    step[pos] = True
                elif not active and count == 3:
                    step[pos] = True
            gen = Conway4D(step, self.n_dim)
        return gen

    def __init__(self, generation, n_dim):
        self.data = generation
        self.n_dim = n_dim


conway = Conway4D.parse(ins, 3)
out = conway.iterate(6)
print(f"Result 1: {len(out.data)}")

conway = Conway4D.parse(ins, 4)
out = conway.iterate(6)
print(f"Result 2: {len(out.data)}")
