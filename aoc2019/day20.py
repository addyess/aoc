from collections import namedtuple
from itertools import takewhile, accumulate
from astar import AStar
from math import sqrt

Portal = namedtuple("Portal", "value, pos, outer")


class Donut(AStar):
    ALPHAS = [chr(_) for _ in range(ord('A'), ord('Z') + 1)]
    RIGHT, LEFT, DOWN, UP = (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0)
    IN, OUT = (0, 0, 1), (0, 0, -1)
    DIRS = [RIGHT, LEFT, DOWN, UP]

    @classmethod
    def parse(cls, lines):
        return cls({
            (x, y): v
            for y, line in enumerate(lines)
            for x, v in enumerate(line)
            if v not in ('#', ' ')
        })

    def mk_size(self):
        xs, ys = zip(*self.coords.keys())
        return min(xs), min(ys), max(xs), max(ys)

    @staticmethod
    def at(pos, inc):
        return tuple(sum(it) for it in zip(pos, inc))

    def mk_portals(self):
        def portal(x, y):
            my_val = self.coords[(x, y)]
            neighs = list(filter(lambda n: n[0] is not None, [
                (self.coords.get(self.at((x, y), _dir)), _dir,) for _dir in self.DIRS
            ]))
            if len(neighs) < 2:
                return
            n_vals, n_dirs = zip(*sorted(neighs, key=lambda p: p[0]))
            if '.' not in n_vals:
                return
            n_val, n_dir = n_vals[1], n_dirs[1]
            if n_dir in [self.LEFT, self.UP]:
                val = ''.join([n_val, my_val])
            elif n_dir in [self.RIGHT, self.DOWN]:
                val = ''.join([my_val, n_val])
            outer = False
            for ox, oy in outers:
                outer = outer or (ox == 0 and y == oy) or (oy == 0 and x == ox)
            return Portal(val, (x, y), outer)

        x1, y1, x2, y2 = self.mk_size()
        outers = [(x1 + 1, 0), (x2 - 1, 0), (0, y1 + 1), (0, y2 - 1)]
        return {p.pos: p for p in filter(None, [
            portal(x, y)
            for y in range(y1, y2+1)
            for x in range(x1, x2+1)
            if self.coords.get((x, y)) in self.ALPHAS
        ])}

    def __init__(self, coords):
        self.coords = coords
        self.shrinks = False
        self.portals = self.mk_portals()
        endpoints = {v.value: p + (0,) for p, v in self.portals.items() if v.value in ['AA', 'ZZ']}
        self.begin, self.end = endpoints['AA'], endpoints['ZZ']

    def neighbors(self, node):
        x, y, z = node
        portal_coord = x, y
        portal = self.portals.get(portal_coord)

        possible = [self.at(node, _dir) for _dir in self.DIRS]
        open_n = list(filter(lambda n: n[0] not in [None] + self.ALPHAS, [
            (self.coords.get((p[0], p[1])), p) for p in possible
        ]))

        def non_portals(p):
            if p and p.value in ['AA', 'ZZ'] and z == 0:
                return True
            elif p is None or (self.shrinks and p.outer and z == 0):
                return False
            return True
        portal_n = list(filter(non_portals, [
            self.portals.get((p[0], p[1])) for p in possible
        ]))
        peer_n = [
            v for v in self.portals.values() if portal and v.value == portal.value and v.pos != portal_coord
        ]

        if self.shrinks and portal:
            z_dim = lambda n: z - 1 if n else z + 1
            open_p = [
                (p.value, p.pos + (z_dim(portal.outer),)) for p in peer_n
            ]
        else:
            open_p = [(p.value, p.pos + (z,)) for p in (portal_n + peer_n)]
        final = (open_n + open_p)
        return set(n[1] for n in final)

    def distance_between(self, n1, n2):
        p1, p2 = (n1[0], n1[1]), (n2[0], n2[1])
        if p1 in self.portals and p2 in self.portals:
            return 1
        elif p1 in self.portals or p2 in self.portals:
            return 0
        return 1

    def heuristic_cost_estimate(self, current, goal):
        x, y, z = self.at(current, goal)
        return sqrt(x ** 2 + y ** 2 + z ** 2)

    def solve(self):
        return self.astar(self.begin, self.end)

    def distance(self, path):
        final = 0
        head, tail = path[0], path[1:]
        while tail:
            final += self.distance_between(head, tail[0])
            head, tail = tail[0], tail[1:]
        return final


def main():
    with open("day20.txt") as fin:
        ins = fin.read()
    lines = takewhile(lambda l: l.strip() != 'EOF', ins.splitlines())
    donut = Donut.parse(lines)

    path = list(donut.solve())
    distance = donut.distance(path)
    print(f"Result 1: {distance}")

    donut.shrinks = True
    path = list(donut.solve())
    distance = donut.distance(path)
    print(f"Result 2: {distance}")


main()
