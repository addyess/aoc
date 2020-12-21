from math import sqrt, prod
from itertools import cycle
from functools import cached_property
from collections import defaultdict, namedtuple
import re

Score = namedtuple('Score', 'tile, side, flipped, score')
LOG_FILE, IN_FILE = "day20.log", "day20.txt"
VERBOSE = True

with open(IN_FILE) as f:
    text = f.read()
tiles_data = text.split("\n\n")


def colorize(char, on=False):
    OKBLUE = '\033[94m'
    MAGEN = '\033[35m'
    ENDC = '\033[0m'
    if char == '█':
        return MAGEN + char + ENDC
    elif char == "#" and on:
        return OKBLUE + char + ENDC
    return char


class Coordinates:
    @staticmethod
    def coord(idx, dim):
        return idx % dim, idx // dim

    def print(self, logfile=None, **kwds):
        if not VERBOSE:
            return
        txt = "\n".join(self.lines(**kwds))
        if logfile:
            with open(logfile, 'w') as f:
                f.write('\033c')
                f.write(txt)
        else:
            print(txt)


class Monster:
    _SEA_MONSTER = """
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """[1:].splitlines()

    @classmethod
    def craft(cls):
        return cls({
            (x, y)
            for y, line in enumerate(cls._SEA_MONSTER)
            for x, char in enumerate(line)
            if char == "#"
        }, len(cls._SEA_MONSTER[0]), len(cls._SEA_MONSTER))

    def __init__(self, data, width, height):
        self.data = data
        self.width, self.height = width, height


class Tile(Coordinates):
    _UUID = re.compile(r"Tile (\d+)")

    @classmethod
    def blank(cls, dim=10):
        return cls(0, dim, {cls.coord(idx, dim): '.' for idx in range(dim * dim)})

    @classmethod
    def assembled(cls, lines, uuid=0):
        return cls(uuid, len(lines), {
            (x, y): char
            for y, line in enumerate(lines)
            for x, char in enumerate(line)
        })

    @classmethod
    def parse(cls, tile_data):
        lines = [_.strip() for _ in tile_data.splitlines()]
        uuid, = cls._UUID.findall(lines[0])
        return cls.assembled(lines[1:], int(uuid))

    def __repr__(self):
        return f"{self.uuid}"

    def __init__(self, uuid, dim, data):
        self.uuid = uuid
        self._data = data
        self._dim = dim

    def lines(self, color=False, borders=False, **_kwds):
        s, e = (0, self._dim) if borders else (1, self._dim - 1)
        return [
            "".join(colorize(self._data[(x, y)], color) for x in range(s, e))
            for y in range(s, e)
        ]

    def side(self, label, flip):
        def value(s):
            t = str.maketrans({'.': '0', '#': '1'})
            b = "".join(s).translate(t)
            return int(b[::-1] if flip else b, 2)

        prop = {
            'l': (self._data[(0, y)] for y in range(self._dim - 1, -1, -1)),
            'r': (self._data[(self._dim - 1, y)] for y in range(self._dim)),
            'b': (self._data[(x, self._dim - 1)] for x in range(self._dim - 1, -1, -1)),
            't': (self._data[(x, 0)] for x in range(self._dim))
        }
        return value(prop[label])

    def scores(self):
        for side in 'rltb':
            for flip in (True, False):
                score = self.side(side, flip)
                yield Score(self, side, flip, score)

    def flip(self):
        """Flip Vertically"""
        data = {(x, self._dim - 1 - y): v for (x, y), v in self._data.items()}
        return Tile(self.uuid, self._dim, data)

    def rr(self):
        """Rotate Right."""
        data = {(self._dim - 1 - y, x): v for (x, y), v in self._data.items()}
        return Tile(self.uuid, self._dim, data)

    def mask(self, monster):
        h, w = monster.height, monster.width
        count = 0
        for x in range(self._dim - w):
            for y in range(self._dim - h):
                locs = [(x + xm, y + ym) for xm, ym in monster.data]
                if all(self._data[_] == "#" for _ in locs):
                    count += 1
                    for _ in locs:
                        self._data[_] = "█"
        return count

    def count(self, char="#"):
        return sum(1 for _ in self._data.values() if _ == char)


class Grid(Coordinates):
    @classmethod
    def craft(cls, tiles):
        dim = int(sqrt(len(tiles)))
        return cls(dim, {
            cls.coord(idx, dim): tile
            for idx, tile in enumerate(tiles)
        })

    @classmethod
    def blank(cls, dim):
        return cls(dim, {
            cls.coord(idx, dim): Tile.blank()
            for idx in range(dim * dim)
        })

    def __init__(self, dim, data):
        self.dim = dim
        self.data = data

    def lines(self, **kwds):
        return [
            "".join(_)
            for y in range(self.dim)
            for _ in zip(*(
                self.data[(x, y)].lines(**kwds) for x in range(self.dim)
            ))
        ]

    def to_tile(self):
        return Tile.assembled(self.lines(color=False))

    def replace(self, idx, tile):
        self.data[self.coord(idx, self.dim)] = tile

    @cached_property
    def scores(self):
        scores = defaultdict(list)
        for tile in self.data.values():
            for score in tile.scores():
                scores[score.score].append(score)
        return scores

    @cached_property
    def corners(self):
        edges = defaultdict(list)
        for score, pieces in self.scores.items():
            if len(pieces) == 1:
                edges[pieces[0].tile].append(pieces[0])
        return dict((t, l) for t, l in edges.items() if len(l) == 4)

    def neighbor(self, tile, side):
        score = next(filter(
            lambda t: not t.flipped and t.side == side, tile.scores()
        ))
        pair = self.scores[score.score]
        return next(p for p in pair if p.tile.uuid != tile.uuid)

    def fill(self):
        to_fill = Grid.blank(self.dim)
        insert = next(
            t for t, tile_scores in self.corners.items()
            if all(_.side in 'lt' for _ in tile_scores)
        )
        snake = cycle(("rl", "bt", "lr", "bt"))
        slot, inc = 0, 1
        for idx in range(self.dim * self.dim):
            to_fill.replace(slot, insert)
            to_fill.print(logfile=LOG_FILE, color=True)
            if idx % self.dim == 0:
                c, n = tuple(next(snake))
            elif idx == (self.dim * self.dim) - 1:
                break
            elif idx % self.dim == self.dim - 1:
                c, n = tuple(next(snake))
                slot = (idx + self.dim + 1) if inc > 0 else idx
                inc = 0 - inc
            next_score = self.neighbor(insert, c)
            next_tile = next_score.tile
            if not next_score.flipped:
                next_tile = next_tile.flip()
            while next_tile.side(n, True) != next_score.score:
                next_tile = next_tile.rr()
            insert = next_tile
            slot += inc
        return to_fill


piece_grid = Grid.craft([Tile.parse(_) for _ in tiles_data])
print(f"Result 1: {prod(s.uuid for s in piece_grid.corners.keys())}")

monster = Monster.craft()
sat_grid = piece_grid.fill()
sat_grid.print(logfile=LOG_FILE, color=True)
sat_tile = sat_grid.to_tile()
while sat_tile.mask(monster) == 0:
    sat_tile = sat_tile.rr()
    sat_tile.print(logfile=LOG_FILE, color=True, borders=True)
sat_tile.print(logfile=LOG_FILE, color=True, borders=True)

print(f"Result 2: {sat_tile.count()}")
