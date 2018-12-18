import logging
from collections import namedtuple
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)-15s: %(message)s', level=logging.INFO)
Loc = namedtuple('Loc', 'y, x')
NTH = 1000000000
WINDOW_SZ = 10   # window of repeated numbers before declaring the whole sequence repeating


class Unit:
    def __init__(self, c):
        self.c = c

    @staticmethod
    def neighbors(loc):
        return {Loc(loc.y + y, loc.x + x) for x in range(-1, 2) for y in range(-1, 2)} - {loc}

    def evaluate(self, grid, loc):
        adj = [u.c for u in filter(None, [grid.get(n) for n in self.neighbors(loc)])]
        if self.c == '.':
            return Unit('|' if adj.count('|') >= 3 else '.')
        elif self.c == '|':
            return Unit('#' if adj.count('#') >= 3 else '|')
        else:
            return Unit('#' if adj.count('#') and adj.count('|') else '.')


class Grid:
    @classmethod
    def construct(cls, txt):
        return Grid({
            Loc(y, x): Unit(c)
            for y, line in enumerate(txt) if line.strip()
            for x, c in enumerate(line.strip())})

    def get(self, item):
        return self.units.get(item)

    @property
    def score(self):
        def reducer(accum, unit):
            yards, logs = accum
            if unit.c == '#':
                return yards+1, logs
            elif unit.c == '|':
                return yards, logs + 1
            return accum
        result = reduce(reducer, self.units.values(), (0,0))
        return result[0] * result[1]

    def __init__(self, units):
        self.units = units
        ys, xs = zip(*self.units.keys())
        self.minx, self.maxx = min(xs), max(xs)
        self.miny, self.maxy = min(ys), max(ys)

    def next(self):
        units = {
            loc: unit.evaluate(self, loc) for loc, unit in self.units.iteritems()
        }
        return Grid(units)

    def __repr__(self):
        r = ''
        for y in range(self.miny, self.maxy + 1):
            r += "{: >3d} ".format(y)
            for x in range(self.minx, self.maxx + 1):
                u = self.units.get((y, x))
                r += u.c + ' '
            r += '\n'
        return r


if __name__ == '__main__':
    logger.info("Start")
    with open('input18.txt') as in_file:
        g = Grid.construct(in_file)

    running_scores, unique_scores = [], set()
    it = 0
    for it in range(10):
        score = g.score
        unique_scores.add(score)
        running_scores += [score]
        g = next(g)
    logger.info("Solution 1: %d", g.score)

    reset = it
    while (it - reset) < WINDOW_SZ:
        score = g.score
        it += 1
        if score not in unique_scores:
            reset = it+1  # location of the next repeated score (where the loop resets)
            unique_scores.add(score)
        running_scores += [score]
        g = next(g)

    start_of_cycle = running_scores.index(running_scores[reset])  # Start of repeated scores
    cycling = running_scores[start_of_cycle:reset]                # List of repeating scores
    index_into = (NTH - start_of_cycle) % len(cycling)            # index into repeated scores
    logger.info("Solution 2: %s", cycling[index_into])
