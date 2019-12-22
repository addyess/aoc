from collections import deque, defaultdict


class Tunnels:
    DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def __init__(self, lines):
        self.coord = {
            (x, y): c
            for y, line in enumerate(lines)
            for x, c in enumerate(line)
            if c != "#"
        }
        self.cur = set(_ for _, v in self.coord.items() if v == '@').pop()

    def bfs(self):
        q = deque()
        q.append((self.cur, 0))
        dest = defaultdict(dict)
        dest[self.cur] = {0: 0}
        best = 0, 0
        while len(q) != 0:
            t_p, t_m = q.pop()
            for d_p in self.DIRS:
                n_p = tuple(sum(it) for it in zip(t_p, d_p))
                what = self.coord.get(n_p)
                if what is None:
                    continue
                if 'A' <= what <= 'Z':
                    if not (t_m & (1 << ord(what)-ord('A'))):
                        continue
                n_m = t_m
                if 'a' <= what <= 'z':
                    n_m |= (1 << ord(what)-ord('a'))
                if n_m in dest[n_p]:
                    continue
                dest[n_p][n_m] = dest[t_p][t_m] + 1
                best = min(best, (-n_m, dest[n_p][n_m]))
                q.append((n_p, n_m))
        return best[1]


def main():
    with open("day18.txt") as fin:
        ins = fin.read()

    #     ins = """
    # ########################
    # #f.D.E.e.C.b.A.@.a.B.c.#
    # ######################.#
    # #d.....................#
    # ########################
    # """

    #     ins = """
    # #################
    # #i.G..c...e..H.p#
    # ########.########
    # #j.A..b...f..D.o#
    # ########@########
    # #k.E..a...g..B.n#
    # ########.########
    # #l.F..d...h..C.m#
    # #################"""
    #
    ins = """
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################"""

#     ins = """
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
    tunnels = Tunnels(lines)
    steps = tunnels.bfs()
    print(f"{steps}")


main()
