from collections import defaultdict as dd

with open("day24.txt") as f_in:
    ins = [_.strip() for _ in f_in]


class Tiles:
    @classmethod
    def parse(cls, text):
        def _break(series):
            while series:
                if series[0] in 'sn':
                    yield series[:2]
                    series = series[2:]
                else:
                    yield series[0]
                    series = series[1:]

        return cls(_break(s) for s in text)

    def __init__(self, sequences, ground=None):
        self.ground = dd(bool, ground.items()) if ground else dd(bool)
        if sequences:
            for seq in sequences:
                pos = 0, 0
                for s in seq:
                    pos = self.neighbor(pos, s)
                self.ground[pos] ^= True
            black_tiles = [k for k, v in self.ground.items() if v]
            maxx, maxy = map(max, zip(*black_tiles))
            minx, miny = map(min, zip(*black_tiles))
            for y in range(miny - 1, maxy + 2):
                for x in range(minx - 1, maxx + 2):
                    _ = self.ground[(x, y)]

    @property
    def sum(self):
        return sum(self.ground.values())

    @staticmethod
    def neighbor(pos, direction):
        (x, y), mod = pos, (1 - pos[1] % 2)
        return {
            "e": (x + 1, y),
            "se": (x + mod, y + 1),
            "sw": (x + mod - 1, y + 1),
            "w": (x - 1, y),
            "ne": (x + mod, y - 1),
            "nw": (x + mod - 1, y - 1),
        }[direction]

    @classmethod
    def next_day(cls, self):
        new = Tiles(None, self.ground)
        to_flip = []
        for pos, v in self.ground.items():
            black = sum(
                new.ground[self.neighbor(pos, _)]
                for _ in ["e", "se", "sw", "w", "ne", "nw"]
            )
            if v and (black == 0 or black > 2):
                to_flip.append(pos)
            elif not v and black == 2:
                to_flip.append(pos)
        for pos in to_flip:
            new.ground[pos] ^= True
        return new


tiles = Tiles.parse(ins)
print(f"Result 1: {tiles.sum}")
for d in range(100):
    tiles = Tiles.next_day(tiles)
print(f"Result 2: {tiles.sum}")
