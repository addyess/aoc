from collections import deque, namedtuple
try:
    from blist import blist
except ImportError:
    blist = list


class Coord(namedtuple('_Coord', 'x y z')):
    def visit(self, c):
        x, y, z = self
        z_set = set(z)
        z_set.update(c)
        return Coord(x, y, ''.join(sorted(z_set)))

    def __contains__(self, c):
        return c in self.z

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
        self.num_keys = len({v for v in self.coord.values() if 'a' <= v <= 'z'})

    def is_open(self, pos, z):
        val = self.coord[pos]
        if 'A' <= val <= 'Z':
            return val.lower() in z
        return True

    def solve(self):
        graph, start = self.graph, self.cur
        # keep track of explored nodes
        explored = []
        # keep track of all the paths to be checked
        queue = deque([[Coord(*start, '')]])

        # keeps looping until all possible paths have been checked
        while queue:
            # pop the first path from the queue
            path = queue.popleft()
            # get the last node from the path
            node = path[-1]
            if node not in explored:
                neighbors = (_ for _ in graph[node.pos] if self.is_open(_, node.z))
                # go through all neighbor nodes, construct a new path and
                # push it into the queue
                for neighbor in neighbors:
                    new_path = blist(path)

                    neigh_coord = Coord(*neighbor, node.z)
                    neigh_val = self.coord[neighbor]
                    if 'a' <= neigh_val <= 'z':
                        neigh_coord = neigh_coord.visit(neigh_val)

                    new_path.append(neigh_coord)
                    queue.append(new_path)

                    if len(neigh_coord.z) == self.num_keys:
                        return new_path

                # mark node as explored
                explored.append(node)


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
    print(f"{len(steps)-1}")


main()
