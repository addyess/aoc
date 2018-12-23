import logging
from collections import namedtuple
from astar import AStar
from math import hypot

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)-15s: %(message)s', level=logging.INFO)
Loc = namedtuple('Loc', 'x, y, z')


class Region(Loc):
    def __new__(cls, x, y, z, cave, **kwargs):
        self = super(Region, cls).__new__(cls, x, y, z)
        return self

    def __init__(self, x, y, z, cave, **kwargs):
        super(Region, self).__init__(x, y, z)
        self.cave = cave
        self._type = kwargs.get('type')
        self._geo_index = kwargs.get('geo_index')
        self._erosion_level = kwargs.get('erosion')

    def at_z(self, z):
        return Region(
            self.x, self.y, z, self.cave,
            geo_index=self.geo_index,
            type=self.type,
            erosion=self.erosion_level
        )

    @property
    def geo_index(self):
        if self._geo_index is None:
            if self in ((0, 0, 0), self.cave.target.loc):
                self._geo_index = 0
            elif self.y == 0:
                self._geo_index = self.x * 16807
            elif self.x == 0:
                self._geo_index = self.y * 48271
            else:
                self._geo_index = self.cave.at(self.x - 1, self.y, 0).erosion_level * \
                                  self.cave.at(self.x, self.y - 1, 0).erosion_level
        return self._geo_index

    @property
    def erosion_level(self):
        if self._erosion_level is None:
            rem = (self.geo_index + self.cave.depth) % 20183
            self._type = rem % 3
            self._erosion_level = rem
        return self._erosion_level

    @property
    def named(self):
        return {0: 'rocky', 1: 'wet', 2: 'narrow'}[self.type]

    @property
    def symbol(self):
        return {0: '.', 1: '=', 2: '|'}[self.type]

    @property
    def type(self):
        if self._type is None:
            _ = self.erosion_level
        return self._type

    @property
    def loc(self):
        return tuple(self)


class Cave(AStar):
    TORCH, CLIMB, NEITHER = 0, 1, 2

    def __init__(self, target, depth):
        self.depth = depth
        self.regions = {}
        self.target = self.at(target[0], target[1], Cave.TORCH)

    def neighbors(self, l):
        def sheer(_loc):
            return _loc[0] >= 0 and _loc[1] >= 0

        points = filter(sheer, [
            (l.x + 1, l.y, l.z),
            (l.x - 1, l.y, l.z),
            (l.x, l.y + 1, l.z),
            (l.x, l.y - 1, l.z),
            (l.x, l.y, (l.z + 1) % 3),
            (l.x, l.y, (l.z + 2) % 3)
        ])
        neighbors = (self.at(*p) for p in points)
        return neighbors

    def distance_between(self, n1, n2):
        """
        TORCH = 0   (rocky 0  or narrow 2)
        CLIMB = 1   (rocky 0 or wet 1 )
        NEITHER = 2 (wet 1 or narrow 2)

        In rocky regions, you can use the climbing gear or the torch. You cannot use neither (you'll likely slip and fall).
        In wet regions, you can use the climbing gear or neither tool. You cannot use the torch (if it gets wet, you won't have a light source).
        In narrow regions, you can use the torch or neither tool. You cannot use the climbing gear (it's too bulky to fit).
        """
        if (
            (n1.z == Cave.TORCH   and n2.type == 1) or  # TORCH cannot go wet
            (n1.z == Cave.CLIMB   and n2.type == 2) or  # CLIMB cannot go narrow
            (n1.z == Cave.NEITHER and n2.type == 0)   # NEITHER cannot go rocky
        ):
            return float('inf')
        if n1.z != n2.z:
            return 7
        return 1

    def heuristic_cost_estimate(self, current, goal):
        x1, y1 = current.x, current.y
        x2, y2 = goal.x, goal.y
        hy = hypot(x2 - x1, y2 - y1)
        if current.z != goal.z:
            hy = hypot(hy, 1)
        return hy

    def at(self, x, y, z):
        z = Cave.TORCH if z is None else z
        r = self.regions.get((x, y, z))
        if z is not 0:
            copy_me = self.regions.get((x, y, 0))
            if copy_me:
                r = copy_me.at_z(z)
                self.regions[r.loc] = r
        if r is None:
            r = Region(x, y, z, self)
            self.regions[r.loc] = r
        return r

    def __repr__(self):
        r = ''
        for y in range(0, self.target.y + 1):
            r += ''.join(self.at(x, y, 0).symbol for x in range(0, self.target.x + 1)) + '\n'
        return 'M' + r[1:-2] + 'T'


def time_trip(moves):
    time = 0
    pre, tail = moves[0], moves[1:]
    for n1 in tail:
        time += 1 if pre.z == n1.z else 7
        pre = n1
    return time


def test():
    target = Loc(10, 10, 0)
    c = Cave(target, 510)
    assert c.at(0, 0, 0).geo_index == 0
    assert c.at(0, 0, 0).erosion_level == 510
    assert c.at(0, 0, 0).named == 'rocky'

    assert c.at(1, 0, 0).geo_index == 16807
    assert c.at(1, 0, 0).erosion_level == 17317
    assert c.at(1, 0, 0).named == 'wet'

    assert c.at(0, 1, 0).geo_index == 48271
    assert c.at(0, 1, 0).erosion_level == 8415
    assert c.at(0, 1, 0).named == 'rocky'

    assert c.at(1, 1, 0).geo_index == 145722555
    assert c.at(1, 1, 0).erosion_level == 1805
    assert c.at(1, 1, 0).named == 'narrow'

    assert c.at(10, 10, 0).geo_index == 0
    assert c.at(10, 10, 0).erosion_level == 510
    assert c.at(10, 10, 0).named == 'rocky'

    path = [(x, y) for x in range(0, target.x + 1) for y in range(0, target.y + 1)]
    assert 114 == sum(c.at(x, y, 0).type for x, y in path)

    r = (list(c.astar(c.at(0, 0, Cave.TORCH), c.target)))
    assert 45 == time_trip(r)


def main():
    logger.info("Start")
    with open('input22.txt') as t:
        depth = int(t.readline().strip('depth: '))
        loc = eval(t.readline().strip('target: '))
        target = Loc(loc[0], loc[1], Cave.TORCH)
    c = Cave(target, depth)

    points = [(x, y) for x in range(0, target.x + 1) for y in range(0, target.y + 1)]
    logger.info("Solution #1: %d", sum(c.at(x, y, 0).type for x, y in points))

    t = list(c.astar(c.at(0, 0, Cave.TORCH), c.target))
    logger.info("Solution #2: %d", time_trip(t))


if __name__ == '__main__':
    test()
    main()
