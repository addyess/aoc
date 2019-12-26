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
    DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    @classmethod
    def parse(cls, lines):
        return cls({
            (x, y): c
            for y, line in enumerate(lines)
            for x, c in enumerate(line)
            if c != "#"
        })

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
        self.graph = self.mk_graph()
        self.cur = set(_ for _, v in self.coord.items() if v == '@').pop()
        self.num_keys = sum(Coord.bit_val(v) for v in self.coord.values() if 'a' <= v <= 'z')

    def is_open(self, pos, node):
        val = self.coord[pos]
        if 'A' <= val <= 'Z':
            return val.lower() in node
        return True

    def solve(self):
        graph, start = self.graph, self.cur
        # keep track of explored nodes
        explored = set()
        # keep track of all the paths to be checked
        queue = deque([Coord(*start, 0)])

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
                    if 'a' <= neigh_val <= 'z':
                        neigh_coord = neigh_coord.visit(neigh_val)

                    queue.append(neigh_coord)

                    if neigh_coord.z == self.num_keys:
                        return neigh_coord

                # mark node as explored
                explored.add(node)


def main():
    with open("day18.txt") as fin:
        ins = fin.read()

#         ins = """
# ########################
# #f.D.E.e.C.b.A.@.a.B.c.#
# ######################.#
# #d.....................#
# ########################
# """
#         ins = """
# ########################
# #@..............ac.GI.b#
# ###d#e#f################
# ###A#B#C################
# ###g#h#i################
# ########################"""
#         ins = """
# #################
# #i.G..c...e..H.p#
# ########.########
# #j.A..b...f..D.o#
# ########@########
# #k.E..a...g..B.n#
# ########.########
# #l.F..d...h..C.m#
# #################"""

    lines = ins.strip().splitlines()
    tunnels = Tunnels.parse(lines)
    steps = tunnels.solve()
    print(f"{steps.dist}")


main()
