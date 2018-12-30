import logging
from collections import namedtuple
import heapq

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)-15s: %(message)s', level=logging.INFO)
Loc = namedtuple('Loc', 'x, y, z')


class Region(Loc):
    ROCKY, WET, NARROW = 0, 1, 2

    def __new__(cls, x, y, z, cave, **kwargs):
        self = super(Region, cls).__new__(cls, x, y, z)
        return self

    def __init__(self, x, y, z, cave, **kwargs):
        super(Region, self).__init__(x, y, z)
        self.cave = cave
        self._geo_index = kwargs.get('geo_index')
        self._erosion_level = kwargs.get('erosion')
        self._type = kwargs.get('type')

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
            if self == self.cave.target:
                self._geo_index = 0
            elif self.y == 0 or self.x == 0:
                self._geo_index = self.x * 16807 + self.y * 48271
            else:
                self._geo_index = self.cave.at((self.x - 1, self.y, 0)).erosion_level * \
                                  self.cave.at((self.x, self.y - 1, 0)).erosion_level
        return self._geo_index

    @property
    def erosion_level(self):
        if self._erosion_level is None:
            self._erosion_level = (self.geo_index + self.cave.depth) % 20183
        return self._erosion_level

    @property
    def type(self):
        if self._type is None:
            self._type = self.erosion_level % 3
        return self._type


class Cave:
    TORCH, CLIMB, NEITHER = 0, 1, 2

    def __init__(self, target, depth):
        self.depth = depth
        self.regions = {}
        self.target = self.at(target)

    def neighbors(self, l):
        def sheer(_loc):
            return _loc[0] >= 0 and _loc[1] >= 0

        def distance_between(n1, n2):
            if any(either in ((Cave.TORCH, Region.WET),
                              (Cave.CLIMB, Region.NARROW),
                              (Cave.NEITHER, Region.ROCKY))
                   for either in [(n1.z, n2.type), (n2.z, n1.type)]):
                return None
            return (1 if n1.z == n2.z else 7), n2

        points = filter(sheer, [
            (l.x + 1, l.y, l.z), (l.x - 1, l.y, l.z),
            (l.x, l.y + 1, l.z), (l.x, l.y - 1, l.z),
            (l.x, l.y, (l.z + 1) % 3), (l.x, l.y, (l.z - 1) % 3)
        ])
        return filter(None, (distance_between(l, self.at(p)) for p in points))

    def at(self, loc):
        r = self.regions.get(loc)
        if not loc[2]:
            copy_me = self.regions.get((loc[0], loc[1], 0))
            if copy_me:
                r = copy_me.at_z(loc[2])
                self.regions[r] = r
        if r is None:
            r = Region(loc[0], loc[1], loc[2], self)
            self.regions[r] = r
        return r

    def dijkstra(self, source, goal):
        visited = {}
        q = []
        heapq.heappush(q, (0, source))

        while q:
            cost, cur = heapq.heappop(q)
            if cur in visited:
                continue
            visited[cur] = cost
            if cur == goal:
                break
            for edge_cost, nxt in self.neighbors(cur):
                ncost = cost + edge_cost
                if nxt not in visited:
                    heapq.heappush(q, (ncost, nxt))
        assert q, 'queue exited normally D:'
        return visited[goal]


def main():
    logger.info("Start")
    with open('input22.txt') as t:
        depth = int(t.readline().strip('depth: '))
        loc = eval(t.readline().strip('target: '))
        target = Loc(loc[0], loc[1], Cave.TORCH)
    c = Cave(target, depth)

    points = [(x, y, 0) for x in range(target.x + 1) for y in range(target.y + 1)]
    s = sum(c.at(p).type for p in points)
    assert s == 11810
    logger.info("Solution #1: %d", s)

    origin = (0, 0, Cave.TORCH)
    t = c.dijkstra(c.at(origin), c.target)
    assert t == 1015
    logger.info("Solution #2: %d", t)


if __name__ == '__main__':
    main()
