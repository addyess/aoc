from itertools import product

with open("day17.txt") as f_in:
    ins = [_.strip() for _ in f_in]


class ConwayND:
    @classmethod
    def parse(cls, initial, n_dim):
        return cls(set(
            (x, y,) + (0,) * (n_dim - 2)
            for y, line in enumerate(initial)
            for x, val in enumerate(line)
            if val == "#"
        ))

    @staticmethod
    def neighbors(pos):
        return filter(
            lambda c: c != pos, product(*(range(d - 1, d + 2) for d in pos))
        )

    def bounds(self):
        mins = map(min, zip(*self.data))
        maxs = map(max, zip(*self.data))
        return product(*(
            range(min_d - 1, max_d + 2)
            for min_d, max_d in zip(mins, maxs)
        ))

    def iterate(self, cycles):
        gen = self
        for _ in range(cycles):
            step = set()
            for pos in gen.bounds():
                active = pos in gen.data
                count = sum(n in gen.data for n in gen.neighbors(pos))
                if active and count in [2, 3]:
                    step.add(pos)
                elif not active and count == 3:
                    step.add(pos)
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
