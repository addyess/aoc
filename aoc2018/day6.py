import logging
import re
import sys
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)-15s: %(message)s', level=logging.INFO)
logger.info("Start")

parse_re = re.compile(r'(\d+), (\d+)')


class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.tot = 0
        self.root = False

    @classmethod
    def from_text(cls, txt):
        p = cls(*map(int, parse_re.search(txt.strip()).groups()))
        p.root = True
        return p

    def dist(self, p):
        return abs(p.x-self.x) + abs(p.y-self.y)

    def __repr__(self):
        return str((self.x, self.y))

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, p):
        return hash(self) == hash(p)


class Grid:
    @classmethod
    def from_file(cls, f):
        g = cls()
        [g.add(l) for l in f]
        return g

    def __init__(self):
        self.x_min, self.y_min = sys.maxint, sys.maxint
        self.x_max, self.y_max = 0, 0
        self.points = []

    def add(self, txt):
        p = Point.from_text(txt)
        self.x_min = min(self.x_min, p.x)
        self.y_min = min(self.y_min, p.y)
        self.x_max = max(self.x_max, p.x)
        self.y_max = max(self.y_max, p.y)
        self.points += [p]
        return p

    def closest(self, p2):
        resp, dist = None, None
        for p1 in self.points:
            pdist = p1.dist(p2)
            p2.tot += pdist
            if dist is None or pdist < dist:
                resp = p1
                dist = pdist
            elif pdist == dist:
                resp = None
        return resp

    def calculate(self, MAX_RANGE):
        point_map = {p: 0 for p in self.points}
        area_within = 0
        corners = [
            self.closest(Point(self.x_min, self.y_min)),
            self.closest(Point(self.x_min, self.y_max)),
            self.closest(Point(self.x_max, self.y_min)),
            self.closest(Point(self.x_max, self.y_max))
        ]

        for y in range(self.y_min, self.y_max+1):
            for x in range(self.x_min, self.x_max+1):
                p2 = Point(x, y)
                p1 = self.closest(p2)
                if p1 and p1 not in corners:
                    point_map[p1] += 1
                if p2.tot < MAX_RANGE:
                    area_within += 1
        largest_area = max(*point_map.values())
        return largest_area, area_within


def main():
    with open('input6.txt') as f:
        g = Grid.from_file(f)

    largest_area, area_within = g.calculate(10000)
    logger.info('Solution #1 -- %d' % largest_area)
    logger.info('Solution #2 -- %d' % area_within)

main()
