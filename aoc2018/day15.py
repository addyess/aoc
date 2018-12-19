import logging
import math
from itertools import ifilter

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)-15s: %(message)s', level=logging.INFO)
ELF_ATTACK = 4

def up(loc): return (loc[0] - 1, loc[1])
def down(loc): return (loc[0] + 1, loc[1])
def left(loc): return (loc[0], loc[1] - 1)
def right(loc): return (loc[0], loc[1] + 1)


class Unit:
    def __init__(self, loc, c):
        self.c = c
        self.loc = loc
        self.locked = False
        self.hits = 200
        self.power = ELF_ATTACK if c == 'E' else 3

    def __repr__(self):
        return "{}({})".format(self.c, self.hits)

    def enemy(self, unit):
        return self.c == 'E' and unit.c == 'G' or \
               self.c == 'G' and unit.c == 'E'

    def attacked(self, power, grid):
        self.hits = self.hits - power
        if self.hits <= 0:
            grid.units[self.loc] = Unit(self.loc, '.')

    @property
    def open(self):
        return self.c == '.'

    def targets(self, grid):
        return (u for u in grid.units.values() if
                self.enemy(u) and len(list(u.open_range(grid))) != 0)

    def range(self, grid):
        return (grid.units.get(f(self.loc)) for f in [down, up, left, right])

    def open_range(self, grid):
        return (_ for _ in self.range(grid) if _ and _.open)

    def enemy_range(self, grid):
        return [_ for _ in self.range(grid) if _ and _.enemy(self)]

    def move(self, grid):
        targets = list(self.targets(grid))
        charts = map(grid.distance, map(lambda t: (self, t), targets))
        best_targets = sorted(filter(None, charts))
        if best_targets:
            _, _, end, chart = best_targets[0]
            p = sorted(chart.shortest_paths(end, grid), key=lambda p: p.loc)
            self.loc = p[0].loc

    def attack(self, grid):
        in_range_enemies = self.enemy_range(grid)
        if in_range_enemies:
            choose = sorted(in_range_enemies, key=lambda u: (u.hits, u.loc))
            choose[0].attacked(self.power, grid)
            return True
        return False

    def evaluate(self, grid):
        self.locked = True
        old = self.loc
        if self.c in 'EG':
            if not self.attack(grid):
                self.move(grid)
                self.attack(grid)
        return old


class Distance(dict):
    def shortest_paths(self, end, grid):
        def prior(cur):
            if self[cur.loc] == 1:
                return {cur}
            s = sorted(cur.open_range(grid), key=lambda t: self.get(t.loc, grid.max))
            filt = filter(lambda t: self.get(t.loc) == self[s[0].loc], s)
            return {x for f in filt for x in prior(f)}
        p = prior(end)
        return list(p)

    def __repr__(self):
        maxx, maxy = 0, 0
        locs = self.keys()
        for y, x in locs:
            maxx = max(maxx, x)
            maxy = max(maxy, y)
        r = ''
        for y in range(maxy + 2):
            r += ' '.join(map(str, (self.get((y, x), '#') for x in range(maxx + 2)))) + '\n'
        return r


class Grid:
    @classmethod
    def construct(cls, txt):
        grid = [list(row.strip()) for row in txt if row]
        units = {
            (y, x): Unit((y, x), c)
            for y, row in enumerate(grid)
            for x, c in enumerate(row)
            if c != '#'
        }
        return cls(units)

    @property
    def max(self):
        return math.ceil((self.maxx * 2 + self.maxy * 2))

    def __init__(self, units):
        self.units = units
        self.maxx, self.maxy = 0, 0
        locs = self.units.keys()
        for y, x in locs:
            self.maxx = max(self.maxx, x)
            self.maxy = max(self.maxy, y)

    def complete(self):
        competitors = [u for u in self.units.values() if not u.open]
        return len(set(c.c for c in competitors)) == 1

    def body_count(self):
        competitors = [u for u in self.units.values() if not u.open]
        return {
            c:len(filter(lambda u: u.c==c, competitors))
            for c in set(c.c for c in competitors)
         }

    def score(self):
        competitors = [u for u in self.units.values() if not u.open]
        return sum((c.hits for c in competitors))

    def distance(self, points):
        def unworthy(u):
            if u is None:
                return False
            return u == end or u.open

        def outer(cur, level):
            for t in ifilter(unworthy, cur.range(self)):
                d = distances.get(t.loc)
                if d is None or level < d:
                    distances[t.loc] = level
                    if t.loc != end.loc:
                        outer(t, level + 1)

        start, end = points
        distances = Distance({start.loc: 0})
        outer(start, 1)
        dist = distances.get(end.loc)
        return (dist, end.loc, end, distances) if dist else None

    def next(self):
        units = self.units
        for loc in sorted(units.keys()):  # Move across x axis, then down y
            unit = units.get(loc)  # Pick Up Piece
            if not unit.open and not unit.locked:  # Open do not evaluate
                units.pop(loc)
                old = unit.evaluate(self)  # Evaluate Action based on loc and surrounding
                if unit.loc != old:  # Piece has moved
                    units[old] = Unit(old, '.')  # Place Empty where unit was
                units[unit.loc] = unit  # Place Piece Back
        for u in units.values():
            u.locked = False
        return Grid(units)

    def __repr__(self):
        r = '\n'
        for y in range(self.maxy + 2):
            units = []
            r += "{: >2d} ".format(y)
            for x in range(self.maxx + 2):
                u = self.units.get((y, x))
                r += u.c if u else '#'
                if u and not u.open:
                    units.append(u)
            if units:
                r += '   ' + ','.join(map(str, units))
            r += '\n'
        r += '   '
        for x in range(self.maxx + 2):
            r += str(x // 10) if x // 10 else ' '
        r += '\n   '
        for x in range(self.maxx + 2):
            r += str(x % 10)
        return r


def complete_game(text, expected):
    g = Grid.construct(text.split('\n'))
    body_count = g.body_count()
    n = 0
    logger.info("--------ELF ATTACK=%d----------", ELF_ATTACK)
    while not g.complete():
        logger.info("Round %s (ELF ATTACK=%s):%s", n, ELF_ATTACK, g)
        g = next(g)
        n += 1
    score = (n-1) * g.score()
    if expected:
        assert score == expected
    elves_lost = body_count.get('E', 0) - g.body_count().get('E', 0)
    logger.info(g)
    logger.info("After %s rounds with ELF ATTACK %s:, Lost %s Elf", n, ELF_ATTACK, elves_lost)
    return score, elves_lost == 0


def main():
    global ELF_ATTACK
    logger.info("Start")
    with open('input15.txt') as in_file:
        m = in_file.read()

    ELF_ATTACK = 3
    sol1, survived = complete_game(m, None)
    logger.info('Solution #1: %s', sol1)

    attack_min, attack_max = 4, 52
    ELF_ATTACK = attack_max
    sol2 = 'unknown'
    while (attack_max - attack_min) > 1:
        logger.info("Attack between %d-%d", attack_min, attack_max)
        sol, survived = complete_game(m, None)
        if survived:
            sol2 = sol
            attack_max = min(attack_max, ELF_ATTACK)
            ELF_ATTACK = ELF_ATTACK - (ELF_ATTACK - attack_min) // 2
        else:
            attack_min = max(attack_min, ELF_ATTACK)
            ELF_ATTACK = ELF_ATTACK + int(math.ceil((float(attack_max) - ELF_ATTACK) / 2))
    logger.info('Solution #2: %s', sol2)


if __name__ == '__main__':
    main()
