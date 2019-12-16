from collections import defaultdict
from random import randint
try:
    from aoc2019.computer import Machine
except ImportError:
    from computer import Machine


class Map:
    EAST = (1,0)
    WEST = (-1,0)
    NORTH = (0, -1)
    SOUTH = (0, 1)

    def __init__(self):
        self.coord = defaultdict(lambda: ('?', float('inf')))
        self.dir = self.EAST
        self.solution, self.pos = None, (0, 0)
        self.prev = (None, None), 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.solution:
            return 5
        if self.dir == self.EAST:
            return 4
        elif self.dir == self.WEST:
            return 3
        elif self.dir == self.SOUTH:
            return 2
        else:
            return 1

    def ana_pos(self, _dir):
        return tuple(sum(it) for it in zip(self.pos, _dir))

    def send(self, val):
        cur_pos = self.ana_pos(self.dir)
        prev_pos, prev_dist = self.prev
        new_dist = prev_dist + 1
        cur_val, cur_dist = self.coord[cur_pos]
        visited = cur_val != '?'
        moved = val in [1, 2]
        if val == 0:    # WALL
            self.coord[cur_pos] = '#', float("inf")
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
        """Prefer an empty box, then prefer a `right` box with a '#' """
        if self.dir == self.EAST:
            rotations = [self.SOUTH, self.WEST, self.NORTH, self.EAST]
        elif self.dir == self.SOUTH:
            rotations = [self.WEST, self.NORTH, self.EAST, self.SOUTH]
        elif self.dir == self.WEST:
            rotations = [self.NORTH, self.EAST, self.SOUTH, self.WEST]
        else:
            rotations = [self.EAST, self.SOUTH, self.WEST, self.NORTH]
        rotations = [(n_dir, self.coord[self.ana_pos(n_dir)]) for n_dir in rotations]
        rotations = [n_dir for n_dir in rotations if n_dir[1][0] not in ['#', 'F']]
        rotations = sorted(rotations, key=lambda n_dir: n_dir[1][0] != '?')
        for n_dir, val in rotations:
            if val[0] == '?':
                self.dir = n_dir
                return
        if randomize and len(rotations) > 2:
            self.dir = rotations[randint(0, len(rotations)-1)][0]
            return
        rotations = sorted(rotations, key=lambda n_dir: self.ana_pos(n_dir[0]) == self.prev[0])
        self.dir = rotations[0][0]

    def size(self):
        keys = self.coord.keys()
        xs, ys = zip(*keys)
        return min(xs), min(ys), max(xs), max(ys)

    def render(self):
        minx, miny, maxx, maxy = self.size()
        for y in range(miny-1, maxy+2):
            line = [self.coord.get((x, y)) or ('?', None) for x in range(minx-1, maxx+2)]
            line = ''.join([x for x, _ in line])
            if self.pos[1] == y:
                if self.dir[1] == 0:
                    pointer = '<' if self.dir == self.WEST else '>'
                else:
                    pointer = '^' if self.dir == self.NORTH else 'v'
                line = line[:self.pos[0]-minx+1] + pointer + line[self.pos[0]-minx+2:]
            if y == 0:
                line = line[:0-minx+1] + "D" + line[0-minx+2:]
            print(line)
        print()

    def distance(self):
        self.render()
        return self.coord[self.solution][1]


with open("day15.txt") as fin:
    ins = fin.read()
da_map = Map()
machine = Machine.decode(ins, da_map, da_map)
machine.run()
print(f"Result 1: {da_map.distance()}")

# system = System.main(ins)
# print(f"Result 2: {0}")
