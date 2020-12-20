from math import sqrt, prod
from collections import defaultdict, namedtuple
import re

sample = False
extension = ('' if not sample else '_sample')
with open(f"day20{extension}.txt") as f:
    text = f.read()
tiles_data = text.split("\n\n")


class Tile:
    _UUID = re.compile(r"Tile (\d+)")

    @classmethod
    def parse(cls, tile_data):
        lines = [_.strip() for _ in tile_data.splitlines()]
        uuid, = cls._UUID.findall(lines[0])
        return cls(int(uuid), {
            (x, y): char
            for y, line in enumerate(lines[1:])
            for x, char in enumerate(line)
        })

    def __repr__(self):
        return f"{self.uuid}"

    @property
    def lines(self):
        title = f"Tile {self.uuid}: "
        content = [
            "".join(self._data[(x, y)] for x in range(0, 10)) + " "
            for y in range(0, 10)
        ]
        return [title] + content + [" " * 11]

    def __init__(self, uuid, data):
        self.uuid = uuid
        self._data = data

    def side(self, label, flip):
        def value(s):
            t = str.maketrans({'.': '0', '#': '1'})
            b = "".join(s).translate(t)
            return int(b[::-1] if flip else b, 2)
        prop = {
            'l': (self._data[(0, y)] for y in range(10)),
            'r': (self._data[(9, y)] for y in range(10)),
            'b': (self._data[(x, 0)] for x in range(10)),
            't': (self._data[(x, 9)] for x in range(10))
        }
        return value(prop[label])

    def flip(self):
        """Flip Vertically"""
        data = {(x, 9 - y): v for (x, y), v in self._data.items()}
        return Tile(self.uuid, data)

    def rr(self):
        """Rotate Right."""
        data = {(9 - y, x): v for (x, y), v in self._data.items()}
        return Tile(self.uuid, data)


class Grid:
    @classmethod
    def craft(cls, tiles):
        dim = int(sqrt(len(tiles)))
        return cls(dim, {
            (idx % dim, idx // dim): tile
            for idx, tile in enumerate(tiles)
        })

    def __init__(self, dim, data):
        self.dim = dim
        self.data = data

    @property
    def lines(self):
        return [
            "".join(_) + "\n"
            for y in range(self.dim)
            for _ in zip(*(self.data[(x, y)].lines for x in range(self.dim)))
        ]

    def print(self, filename=None):
        with open(filename, 'w') as fw:
            fw.write('\033c')
            fw.writelines(self.lines)

    def at(self, pos):
        return self.data[pos]

    def flip(self, idx):
        pos = (idx // self.dim, idx % self.dim)
        self.data[pos] = self.data[pos].flip()
        return self.data[pos]

    def rr(self, idx):
        pos = (idx % self.dim, idx // self.dim)
        self.data[pos] = self.data[pos].rr()
        return self.data[pos]

    def swap(self, idx1, idx2):
        data = dict(self.data.items())
        pos1 = (idx1 % self.dim, idx1 // self.dim)
        pos2 = (idx2 % self.dim, idx2 // self.dim)
        data[pos2], data[pos1] = data[pos1], data[pos2]
        return Grid(self.dim, data)

    def corners(self):
        pos = [(0, 0), (0, self.dim - 1), (self.dim - 1, 0), (self.dim - 1, self.dim - 1)]
        return [self.data[_] for _ in pos]

    def neighbors(self, x, y):
        pos = [(x - 1, y, "lr"), (x + 1, y, "rl"), (x, y - 1, "tb"), (x, y + 1, "bt")]
        return [(self.data[(x, y)], r) for x, y, r in pos if (x, y) in self.data]

    @property
    def alignment(self):
        for y in range(0, self.dim):
            for x in range(0, self.dim):
                my = self.data[(x, y)]
                for tile, rel in self.neighbors(x, y):
                    if not all(
                            p1 == p2
                            for p1, p2 in zip(my.line(rel[0]), tile.line(rel[1]))
                    ):
                        return False


grid = Grid.craft([Tile.parse(_) for _ in tiles_data])
LOG_FILE = f"day20{extension}.log"
scores = defaultdict(list)
Score = namedtuple('Score', 'tile, flipped')

for tile in grid.data.values():
    for side in 'rltb':
        for flip in (True, False):
            s = tile.side(side, flip)
            scores[s].append(Score(tile, flip))

single_sided = defaultdict(list)
for score, pieces in scores.items():
    if len(pieces) == 1:
        single_sided[pieces[0].tile].append(score)

print(f"Result 1: {prod(s.uuid for s,l in single_sided.items() if len(l)==4)}")