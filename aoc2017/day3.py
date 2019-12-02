def level(pos):
    i = 1
    while i ** 2 < pos:
        i += 2
    return i


def corners(lvl):
    sqr = lvl ** 2
    return reversed([(sqr - (lvl - 1) * n) for n in range(4)])


def dist_from_corner(pos, lvl):
    return min([abs(_ - pos) for _ in corners(lvl)])


def dist(pos):
    lvl = level(pos)
    corner_dist = dist_from_corner(pos, lvl)
    return lvl - 1 - corner_dist


class Chain:
    def __init__(self):
        self.index_map = {}

    def surrounding(self, x, y):
        if (x, y) == (0, 0):
            return 1
        loc = [(-1, -1), (-1, 0), (-1, 1),
               (0, 1), (0, -1),
               (1, -1), (1, 0), (1, 1)]
        vals = [self.index_map.get((x + dx, y + dy)) for dx, dy in loc]
        return sum([val[1] for val in vals if val])

    @staticmethod
    def next_direction(pos, rn, dx, dy):
        cnr = corners(level(pos))
        if pos == next(cnr):
            rn, dx, dy = False, -1, 0
        elif pos == next(cnr):
            rn, dx, dy = False, 0, -1
        elif pos == next(cnr):
            rn, dx, dy = False, 1, 0
        elif pos == next(cnr):
            rn, dx, dy = True, dx, dy
        elif rn:
            rn, dx, dy = False, 0, 1
        return rn, dx, dy

    def value(self, end):
        value = -1
        pos, x, y = 1, 0, 0
        rn, dx, dy = True, 1, 0
        while value <= end:
            value = self.surrounding(x, y)
            self.index_map[x, y] = pos, value
            pos, x, y = pos + 1, x + dx, y + dy
            rn, dx, dy = self.next_direction(pos, rn, dx, dy)
        return value


res1 = dist(347991)
print(f"Result 1: {res1}")

res2 = Chain().value(347991)
print(f"Result 2: {res2}")
