import logging
import re

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)-15s: %(message)s', level=logging.INFO)

SPRING = 500
HORIZ = re.compile(r'y=(\d+), x=(\d+)..(\d+)')
VERT = re.compile(r'x=(\d+), y=(\d+)..(\d+)')


def up(loc): return loc[0] - 1, loc[1]
def down(loc): return loc[0] + 1, loc[1]
def left(loc): return loc[0], loc[1] - 1
def right(loc): return loc[0], loc[1] + 1


class Unit:
    def __init__(self, loc, c):
        self.loc, self.c = loc, c

    def __repr__(self):
        return '(%d, %d)' % self.loc

    @property
    def y(self):
        return self.loc[0]

    @property
    def x(self):
        return self.loc[1]

    @classmethod
    def horizontal(cls, horiz):
        y, x1, x2 = map(int, horiz.groups())
        return [cls((y, x), '#') for x in range(x1, x2+1)]

    @classmethod
    def vertical(cls, vert):
        x, y1, y2 = map(int, vert.groups())
        return [cls((y, x), '#') for y in range(y1, y2+1)]

    @staticmethod
    def vein(txt):
        horiz = HORIZ.match(txt)
        return Unit.horizontal(horiz) if horiz else Unit.vertical(VERT.match(txt))


class Grid:
    @classmethod
    def construct(cls, txt):
        cells = [cell for l in filter(None,txt) for cell in Unit.vein(l)]
        return cls({c.loc: c for c in cells})

    def __init__(self, units):
        self.units = units
        ys, _ = zip(*self.units.keys())
        self.miny, self.maxy = min(ys), max(ys)

    def at(self, loc):
        return self.units.get(loc) or Unit(loc, '.')

    @property
    def wet_area(self):
        return len([u for u in self.units.values() if u.c in '|~'])

    @property
    def drained_area(self):
        return len([u for u in self.units.values() if u.c in '~'])

    def insert(self, it):
        # insert wet into sand below loc
        while it.c in '.|' and it.y <= self.maxy:
            self.units[it.loc] = Unit(it.loc, '|')
            it = self.at(down(it.loc))

        if it.y <= self.maxy and it.c in '#~':
            return self.widen_above, (it,)

    def widen_above(self, it):
        lit, a_lit = it, Unit((0, 0), '.')
        rit, a_rit = lit, a_lit
        while lit.c in '~#' and a_lit.c != "#":
            loc = left(lit.loc)
            lit, a_lit = self.at(loc), self.at(up(loc))

        while rit.c in '~#' and a_rit.c != "#":
            loc = right(rit.loc)
            rit, a_rit = self.at(loc), self.at(up(loc))

        # find bucket or ledge
        bucket = a_lit.c == '#' and a_rit.c == "#"
        l_ledge = lit.c in '.|'
        r_ledge = rit.c in '.|'

        if bucket:
            for x in range(a_lit.x+1, a_rit.x):
                self.units[(a_lit.y, x)] = Unit((a_lit.y, x), '~')
            return self.insert, (self.at(up(it.loc)),)
        if l_ledge and r_ledge:
            for x in range(lit.x, rit.x+1):
                self.units[(it.y-1, x)] = Unit((it.y-1, x), '|')
            return self.insert, (lit, rit)
        if l_ledge:
            for x in range(lit.x, rit.x):
                self.units[(it.y-1, x)] = Unit((it.y-1, x), '|')
            return self.insert, (lit,)
        if r_ledge:
            for x in range(lit.x+1, rit.x+1):
                self.units[(it.y-1, x)] = Unit((it.y-1, x), '|')
            return self.insert, (rit,)
        raise UserWarning("This should never be reached")

    def flow(self):
        trampolines = {(self.insert, (self.at(down((self.miny - 1, 500))),))}
        while trampolines:
            nexts = set()
            for fn, positions in trampolines:
                for pos in positions:
                    term = fn(pos)
                    if term:
                        nexts.add(term)
            trampolines = nexts


if __name__ == '__main__':
    logger.info("Start")
    with open('input17.txt') as in_file:
        grid = Grid.construct(in_file)

    grid.flow()
    logger.info("Solution #1: %s", grid.wet_area)
    logger.info("Solution #2: %s", grid.drained_area)
