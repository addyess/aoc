from math import prod

with open("day12.txt") as f_in:
    ins = [_.strip() for _ in f_in]


def sum_tup(*args):
    return tuple(map(sum, zip(*args)))


def prod_tup(lh_val, tup):
    if type(lh_val) is int:
        return tuple(lh_val * _ for _ in tup)
    if type(lh_val) is tuple:
        return tuple(map(prod, zip(lh_val, tup)))


def rev_tup(tup):
    return tuple(reversed(tup))


class Nav:
    COMPASS = {
        'N': lambda v: (0, 0 - v),
        'E': lambda v: (v, 0),
        'S': lambda v: (0, v),
        'W': lambda v: (0 - v, 0)
    }

    @classmethod
    def parse(cls, coords):
        return cls([
            (action[0], int(action[1:])) for action in coords
        ])

    def __init__(self, actions):
        self.actions = actions
        self.pos, self.head = None, None
        self.reset()

    def reset(self, heading=(1, 0)):
        self.pos = 0, 0
        self.head = heading

    def positional(self, cmd, value):
        addend = self.COMPASS[cmd](value)
        self.pos = sum_tup(self.pos, addend)

    def waypoint(self, cmd, value):
        addend = self.COMPASS[cmd](value)
        self.head = sum_tup(self.head, addend)

    def run(self, cardinals):
        for action in self.actions:
            cmd, value = action
            if value == 180 and cmd in 'RL':
                self.head = prod_tup(-1, self.head)
            elif value in [90, 270] and cmd in 'RL':
                if value == 270:
                    cmd = 'R' if cmd == 'L' else 'L'
                mul = (1, -1) if cmd == 'L' else (-1, 1)
                self.head = prod_tup(mul, rev_tup(self.head))
            elif cmd == 'F':
                self.pos = sum_tup(self.pos, prod_tup(value, self.head))
            else:
                cardinals(cmd, value)

    @property
    def manhattan(self):
        return sum(map(abs, self.pos))


nav = Nav.parse(ins)
nav.run(nav.positional)
print(f"Result 1: {nav.manhattan}")

nav.reset((10, -1))
nav.run(nav.waypoint)
print(f"Result 2: {nav.manhattan}")
