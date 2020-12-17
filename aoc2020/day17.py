from collections import defaultdict
from itertools import product

with open("day17.txt") as f_in:
    ins = [_.strip() for _ in f_in]


class ConwayND:
    @classmethod
    def parse(cls, initial, n_dim):
        return cls(defaultdict(bool, (
            ((x, y,) + (0,) * (n_dim - 2), True)
            for y, line in enumerate(initial)
            for x, val in enumerate(line)
            if val == "#"
        )))

    @staticmethod
    def neighbors(pos):
        return filter(
            lambda coord: coord != pos,
            product(*(range(d - 1, d + 2) for d in pos))
        )

    def bounds(self):
        mins = map(min, zip(*self.data.keys()))
        maxs = map(max, zip(*self.data.keys()))
        return product(*(
            range(min_d - 1, max_d + 2)
            for min_d, max_d in zip(mins, maxs)
        ))

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
            gen = ConwayND(step)
        return gen

    def __init__(self, generation):
        self.data = generation


conway = ConwayND.parse(ins, 3)
out = conway.iterate(6)
print(f"Result 1: {len(out.data)}")

conway = ConwayND.parse(ins, 4)
out = conway.iterate(6)
print(f"Result 2: {len(out.data)}")
