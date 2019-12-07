from itertools import zip_longest
with open("day6.txt") as fin:
    ins = fin.read()


class Graph:
    def __init__(self, txt):
        items = (_.split(')') for _ in txt.strip().splitlines())
        self.d = {c: p for p, c in items}

    def path_to_com(self, node):
        p = self.d.get(node)
        if not p:
            return []
        return self.path_to_com(p) + [p]

    def total_orbits(self):
        orbits = set()
        for c, p in self.d.items():
            orbits.add((p, c))
            orbits.update((_, c) for _ in self.path_to_com(p))
        return len(orbits)

    def distance(self, a, b):
        idx, ca, cb = 0, None, None
        pa, pb = (self.path_to_com(self.d[_]) for _ in [a, b])
        for idx, (ca, cb) in enumerate(zip_longest(pa, pb)):
            if ca != cb:
                break
        if ca == cb:
            return 0
        unique_pa, unique_pb = pa[idx-1:], pb[idx-1:]
        return len(unique_pa) + len(unique_pb)


g = Graph(ins)
print(f"Result 1: {g.total_orbits()}")
print(f"Result 2: {g.distance('YOU', 'SAN')}")
