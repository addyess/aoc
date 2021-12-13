from collections import defaultdict


class Cave:
    def __init__(self, lines):
        self.map = defaultdict(set)
        for line in lines:
            rm1, rm2 = map(str.strip, line.split("-"))
            self.map[rm1] |= {rm2}
            self.map[rm2] |= {rm1}

    def search(self, from_room, last_path, last_seen, twice=None):
        all_paths = set()
        seen, path = last_seen | {from_room}, last_path + [from_room]
        for name in self.map[from_room]:
            small = name.lower() == name
            if name == "end":
                all_paths |= {",".join(path + [name])}
            elif (
                not small
                or (small and name not in seen)
                or (name == twice and path.count(name) < 2)
            ):
                all_paths |= self.search(name, path, seen, twice)
        return all_paths

    @property
    def paths(self):
        return self.search("start", [], set())

    @property
    def paths_2(self):
        take2 = {_ for _ in self.map if _ not in ["start", "end"] and _ == _.lower()}
        take2 |= {None}
        return {_ for t in take2 for _ in self.search("start", [], set(), t)}


with open("day12.txt") as fin:
    cave = Cave(fin)
res1 = cave.paths
print(f"Result 1: {len(res1)}")
res2 = cave.paths_2
print(f"Result 2: {len(res2)}")
