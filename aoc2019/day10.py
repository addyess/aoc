from itertools import cycle, count
with open("day10.txt") as fin:
    ins = fin.readlines()


def merge(it1,it2):
    while True:
        yield next(it1)
        yield next(it2)


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def simplify_fraction(p1, p2):
    (x1, y1), (x2, y2) = p1, p2
    numer, denom = x1 - x2, y1 - y2
    common_divisor = gcd(numer, denom)
    return numer // common_divisor, denom // common_divisor


def slope(line):
    it = iter(line)
    x1, y1 = next(it)
    x2, y2 = next(it)
    try:
        return (y2-y1)/(x1-x2)
    except ZeroDivisionError:
        return float('inf')


class Map:
    def __init__(self, txt):
        positions = {}
        for y, row in enumerate(txt):
            for x, c in enumerate(row):
                if c == '#':
                    positions[x, y] = []
        self.positions = positions

    def lines(self, pos):
        lines = self.positions[pos]
        if not lines:
            visitors = list(set(self.positions.keys()) - set([pos]))
            for idx, visit in enumerate(visitors):
                if any(visit in _ for _ in lines):
                    continue
                frac = simplify_fraction(pos, visit)
                line = [pos, visit] + [
                    hidden
                    for hidden in (set(visitors[idx+1:]) - set([visit]))
                    if frac == simplify_fraction(pos, hidden)
                ]
                lines.append(sorted(line))
        return lines

    def can_see(self, pos):
        return sum([
            1 if (line[0] == pos or line[-1] == pos) else 2
            for line in self.lines(pos)
        ])

    def best_pos(self):
        seen_pos = 0, (0, 0)
        for pos in set(self.positions.keys()):
            seen_pos = max((self.can_see(pos), pos), seen_pos)
        return seen_pos

    def vaporize(self, pos, max_count):
        by_slope = sorted([(slope(_), _) for _ in self.lines(pos)], reverse=True)
        cur_count, num_lines = 0, len(by_slope)
        depth = merge(count(1), count(-1, -1))
        for l_idx, (l_slope, line) in enumerate(cycle(by_slope)):
            if l_idx % num_lines == 0:
                next_depth = next(depth)
            next_dir = -1 if (l_slope == float('inf')) else 1
            remove_pos = line.index(pos) + next_dir*next_depth
            if 0 <= remove_pos < len(line):
                max_count -= 1
                if max_count == 0:
                    x, y = line[remove_pos]
                    return x*100 + y


map = Map(ins)
best_count, best_pos = map.best_pos()
print(f"Result 1: {best_count}")
print(f"Result 2: {map.vaporize(best_pos, 200)}")
