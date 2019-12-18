from collections import defaultdict
from random import randint
from itertools import count

try:
    from aoc2019.computer import Machine
except ImportError:
    from computer import Machine


class System:
    A, B, C, CM, END = 'A', 'B', 'C', ',', '\n'
    L, R = 'L', 'R'
    AS_COORD = {"^": (0, -1), "<": (-1, 0), "v": (0, 1), ">": (1, 0)}
    NEXT = {
        (( 0, -1), (-1,  0)): L,  # ^ -- < is left
        (( 0, -1), ( 1,  0)): R,  # ^ -- > is right
        ((-1,  0), ( 0, -1)): R,  # < -- ^ is right
        ((-1,  0), ( 0,  1)): L,  # < -- v is left
        (( 1,  0), ( 0, -1)): L,  # > -- ^ is left
        (( 1,  0), ( 0,  1)): R,  # > -- v is right
        (( 0,  1), (-1,  0)): R,  # v -- < is right
        (( 0,  1), ( 1,  0)): L,  # v -- > is left
    }

    def __init__(self):
        self.robo = None
        self.pos = 0, 0
        self.coord = {}
        self.x_spots = []
        self.path = []
        self.commands = iter([])
        self.score = 0

    def __iter__(self):
        return self

    def __next__(self):
        return ord(next(self.commands))

    def send(self, val):
        if val > 127:
            self.score = val
            return
        a_val = chr(val)
        if a_val in ['^', '<', '>', 'v', 'X']:
            self.robo = self.pos, a_val
        if a_val in ['^', '<', '>', 'v', '#']:
            self.coord[self.pos] = '#'
        self.pos = self.plus(self.pos, (1, 0))
        if a_val == '\n':
            self.pos = 0, self.pos[1] + 1

    def size(self):
        xs, ys = zip(*self.coord.keys())
        return min(xs), min(ys), max(xs), max(ys)

    def at(self, pos):
        return self.coord.get(pos) or '.'

    @staticmethod
    def plus(pos, dir):
        return tuple(sum(it) for it in zip(pos, dir))

    @staticmethod
    def minus(pos_a, pos_b):
        return tuple(a - b for a, b in zip(pos_a, pos_b))

    def align(self):
        minx, miny, maxx, maxy = self.size()
        self.x_spots = [
            (x, y)
            for y in range(miny, maxy + 1)
            for x in range(minx, maxx + 1)
            if self.at((x, y)) == '#' and all([
                '#' == self.at(self.plus((x, y), dir))
                for dir in [(0, 1), (0, -1), (1, 0), (-1, 0)]]
            )
        ]
        return self.x_spots

    def render(self):
        minx, miny, maxx, maxy = self.size()
        robo, robo_dir = self.robo
        for y in range(miny, maxy + 1):
            line = ''.join([self.at((x, y)) for x in range(minx, maxx + 1)])
            if robo[1] == y:
                line = line[:robo[0] - minx] + robo_dir + line[robo[0] - minx + 1:]
            print(line)
        print()

    def long_path(self):
        pos, val = self.robo
        dir = self.AS_COORD[val]
        path = []
        end = False
        while not end:
            if '#' != self.at(self.plus(pos, dir)):
                choices = set([
                    self.plus(pos, _)
                    for _ in [(0, 1), (0, -1), (1, 0), (-1, 0)]
                    if '#' == self.at(self.plus(pos, _))
                ]) - {self.minus(pos, dir)}
                if len(choices) == 0:
                    end = True
                    continue
                next_dir = self.minus(choices.pop(), pos)
                next_val = self.NEXT[(dir, next_dir)]
                path += [next_val, 0]
                dir = next_dir
            else:
                path = path[:-1] + [(path[-1] + 1)]
                pos = self.plus(pos, dir)
        self.path = path
        return


def main():
    with open("day17.txt") as fin:
        ins = fin.read()

    sys = System()
    machine = Machine.decode(ins, sys, sys)
    machine.run()
    alignments = sys.align()
    print(f"Result 1: {sum(x * y for x, y in alignments)}")

    sys.long_path()
    commands = (ord(_) for _ in
        'A,A,B,B,C,B,C,B,C,A\n'
        'L,10,L,10,R,6\n'
        'R,12,L,12,L,12\n'
        'L,6,L,10,R,12,R,12\n'
        'n\n'
    )
    machine = Machine.decode(ins, commands)
    machine.locs[0] = 2  # Enable input
    machine.run()
    print(f"Result 2: {machine.stdout[-1]}")


main()
