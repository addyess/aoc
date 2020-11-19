from collections import deque, namedtuple

try:
    from blist import blist
except ImportError:
    blist = list


class Coord(namedtuple('_Coord', 'x y z')):
    def __new__(cls, *args, **kwargs):
        dist = kwargs.pop('dist', 0)
        self = super(Coord, cls).__new__(cls, *args, **kwargs)
        self.dist = dist
        return self

    @staticmethod
    def bit_val(c):
        return 1 << (ord(c) - ord('a'))

    def visit(self, c):
        x, y, z = self
        return Coord(x, y, z | self.bit_val(c), dist=self.dist)

    def __contains__(self, c):
        return self.bit_val(c) & self.z

    @property
    def pos(self):
        return self.x, self.y


class Tunnels:
    DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1),]

    @classmethod
    def parse(cls, lines, vaulted=False):
        graph = {
            (x, y): c
            for y, line in enumerate(lines)
            for x, c in enumerate(line)
            if c != "#"
        }
        if vaulted:
            ysize = len(lines) // 2
            xsize = len(lines[0]) // 2
            graph[(xsize+1, ysize+1)] = '@'
            graph[(xsize-1, ysize-1)] = '@'
            graph[(xsize+1, ysize-1)] = '@'
            graph[(xsize-1, ysize+1)] = '@'
            partitions = [
                {k: v for k, v in graph.items() if k[0] < xsize and k[1] < ysize},
                {k: v for k, v in graph.items() if k[0] > xsize and k[1] < ysize},
                {k: v for k, v in graph.items() if k[0] < xsize and k[1] > ysize},
                {k: v for k, v in graph.items() if k[0] > xsize and k[1] > ysize},
            ]
        else:
            partitions = [graph]

        return [cls(_) for _ in partitions]

    @staticmethod
    def pos(a, b):
        return tuple(sum(it) for it in zip(a, b))

    def at(self, a):
        return self.coord.get(a)

    def mk_graph(self):
        graph = {}
        for a in self.coord.keys():
            dirs = [self.pos(a, _) for _ in Tunnels.DIRS]
            vals = [_ for _ in dirs if self.coord.get(_)]
            graph[a] = vals
        return graph

    def __init__(self, coord):
        self.coord = coord
        self.cur = set(_ for _, v in self.coord.items() if v == '@').pop()
        self.graph = self.mk_graph()
        self.keys = set(v for v in self.coord.values() if 'a' <= v <= 'z')
        self.num_keys = sum(Coord.bit_val(v) for v in self.keys)
        self.doors = set(v.upper() for v in self.keys)
        pass

    def is_open(self, pos, node):
        val = self.coord[pos]
        if val in self.doors:
            return val.lower() in node
        return True

    def solve(self):
        graph, starts = self.graph, self.cur
        # keep track of explored nodes
        explored = set()
        # keep track of all the paths to be checked
        queue = deque([Coord(*starts, 0)])

        # keeps looping until all possible paths have been checked
        while queue:
            # pop the first path from the queue
            node = queue.popleft()
            # get the last node from the path
            if node not in explored:
                neighbors = (_ for _ in graph[node.pos] if self.is_open(_, node))
                # go through all neighbor nodes, construct a new path and
                # push it into the queue
                for neighbor in neighbors:
                    neigh_coord = Coord(*neighbor, node.z, dist=node.dist + 1)
                    neigh_val = self.coord[neighbor]
                    if neigh_val in self.keys:
                        neigh_coord = neigh_coord.visit(neigh_val)

                    queue.append(neigh_coord)

                    if neigh_coord.z == self.num_keys:
                        return neigh_coord

                # mark node as explored
                explored.add(node)

    def size(self):
        xs, ys = zip(*self.coord.keys())
        return min(xs), min(ys), max(xs), max(ys)

    def render(self):
        minx, miny, maxx, maxy = self.size()
        for y in range(miny, maxy + 1):
            line = [self.coord.get((x, y)) or '#' for x in range(minx, maxx + 1)]
            print(''.join(line))
        print()


def main():
    with open("day18.txt") as fin:
        ins = fin.read()

    lines = ins.strip().splitlines()
    tunnels = Tunnels.parse(lines)
    steps = sum(_.solve().dist for _ in tunnels)
    print(f"Result 1: {steps}")

    lines = ins.strip().splitlines()
    tunnels = Tunnels.parse(lines, True)
    steps = sum(_.solve().dist for _ in tunnels)
    print(f"Result 2: {steps}")
    # correct answer was 1222 -- i've got a one-off bug somewhere???


main()
