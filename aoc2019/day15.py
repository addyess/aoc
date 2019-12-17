from collections import defaultdict
from random import randint
from itertools import count

try:
    from aoc2019.computer import Machine
except ImportError:
    from computer import Machine


class Map:
    EAST = (1, 0)
    WEST = (-1, 0)
    NORTH = (0, -1)
    SOUTH = (0, 1)

    def __init__(self, coord=None):
        self.coord = coord or defaultdict(lambda: ('?', float('inf')))
        self.dir = self.EAST
        self.solution = [k for k, v in self.coord.items() if v[0] == 'F'][0] if coord else None
        self.pos = 0, 0
        self.prev = (None, None), 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.solution:
            known = len([k for k, v in self.coord.items() if v[0] != '?'])
            if known > 1658:
                return 5
        if self.dir == self.EAST:
            return 4
        elif self.dir == self.WEST:
            return 3
        elif self.dir == self.SOUTH:
            return 2
        else:
            return 1

    def ana_pos(self, _dir, alt=None):
        return tuple(sum(it) for it in zip(alt or self.pos, _dir))

    def send(self, val):
        cur_pos = self.ana_pos(self.dir)
        _, prev_dist = self.prev
        new_dist = prev_dist + 1
        cur_val, cur_dist = self.coord[cur_pos]
        visited = cur_val != '?'
        moved = val in [1, 2]
        if val == 0:  # WALL
            self.coord[cur_pos] = '#', 0
        elif val == 1:  # FREE
            self.coord[cur_pos] = '.', min(new_dist, cur_dist)
        elif val == 2:  # FOUND
            self.coord[cur_pos] = 'F', min(new_dist, cur_dist)
            self.solution = cur_pos
        if moved:
            self.prev = self.pos, min(new_dist, cur_dist)
            self.pos = cur_pos
        self.turn(visited)

    def turn(self, randomize):
        if self.dir == self.EAST:
            rotations = [self.EAST, self.SOUTH, self.WEST, self.NORTH]
        elif self.dir == self.SOUTH:
            rotations = [self.SOUTH, self.WEST, self.NORTH, self.EAST]
        elif self.dir == self.WEST:
            rotations = [self.WEST, self.NORTH, self.EAST, self.SOUTH, ]
        else:
            rotations = [self.NORTH, self.EAST, self.SOUTH, self.WEST]
        adjacent = [(n_dir, self.coord[self.ana_pos(n_dir)]) for n_dir in rotations]
        adjacent = [n_dir for n_dir in adjacent if n_dir[1][0] not in ['#', 'F']]  # Eliminate walls
        adjacent = sorted(adjacent, key=lambda n_dir: n_dir[1][0] != '?')          # Prioritize unknowns
        for n_dir, val in adjacent:
            if val[0] == '?':
                self.dir = n_dir
                return
        if randomize and len(adjacent) > 2:                                        # if 3 or choices, random I guess
            self.dir = adjacent[randint(0, len(adjacent) - 1)][0]
            return
        # if 1 or 2, avoid backtracking if possible, can't help a dead end
        adjacent = sorted(adjacent, key=lambda n_dir: self.ana_pos(n_dir[0]) == self.prev[0])
        self.dir = adjacent[0][0]

    def size(self):
        xs, ys = zip(*self.coord.keys())
        return min(xs), min(ys), max(xs), max(ys)

    def render(self):
        minx, miny, maxx, maxy = self.size()
        for y in range(miny, maxy + 1):
            line = [self.coord.get((x, y)) or ('?', None) for x in range(minx, maxx + 1)]
            line = ''.join([x for x, _ in line])
            if self.pos[1] == y:
                if self.dir[1] == 0:
                    pointer = '<' if self.dir == self.WEST else '>'
                else:
                    pointer = '^' if self.dir == self.NORTH else 'v'
                line = line[:self.pos[0] - minx] + pointer + line[self.pos[0] - minx + 1:]
            if y == 0:
                line = line[:0 - minx] + "D" + line[1 - minx:]
            print(line)
        print()

    def distance(self):
        self.render()
        return self.coord[self.solution][1]

    def flood(self):
        oxygenate = set([self.solution])
        adjacent = [self.EAST, self.WEST, self.NORTH, self.SOUTH]
        for idx in count():
            oxygenate = set(
                self.ana_pos(n_dir, each)
                for each in oxygenate
                for n_dir in adjacent
                if self.coord[self.ana_pos(n_dir, each)][0] == '.'
            )
            for it in oxygenate:
                self.coord[it] = "O", None
            if not oxygenate:
                return idx


def craft_map():
    with open("day15.txt") as fin:
        ins = fin.read()
    da_map = Map()
    machine = Machine.decode(ins, da_map, da_map)
    machine.run()
    out = dict(da_map.coord)
    with open("day15.map", 'w') as f_out:
        f_out.write(str(out))
    return out


def main():
    try:
        with open("day15.map") as fin:
            out = Map(eval(fin.read()))
    except FileNotFoundError:
        out = Map(craft_map())

    print(f"Result 1: {out.distance()}")
    print(f"Result 2: {out.flood()}")


main()
