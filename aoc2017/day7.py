import re

with open("day7.txt") as fin:
    ins = fin.readlines()
name_re = re.compile(r"(\S+)\s+\((\d+)\)")


class Discs:
    def __init__(self, _ins):
        kids = {}
        programs = {}
        for resp in _ins:
            line = resp.strip().split(" -> ")
            name, weight = name_re.match(line[0]).groups()
            children = []
            if len(line) > 1:
                children = line[1].split(", ")
                for kid in children:
                    kids[kid] = name
            programs[name] = int(weight), 0, children

        self.programs = programs
        self.by_kids = kids
        self.any_kid = kid

    def parent(self, prog):
        while prog in self.by_kids:
            prog = self.by_kids[prog]
        return prog

    def weight(self, node=None):
        if node is None:
            node = discs.parent(discs.any_kid)

        reported_weight, _, kids = self.programs[node]
        calc_weight = reported_weight
        tower = [self.weight(_) for _ in kids]
        if tower:
            if max(tower) == min(tower):
                calc_weight += sum(tower)
            else:
                weights = sorted(set(tower), key=tower.count)
                diff = weights[0] - weights[1]
                bad_kid = kids[tower.index(weights[0])]
                bad_weight, _, _ = self.programs[bad_kid]
                raise TypeError(bad_weight - diff)
        self.programs[node] = reported_weight, calc_weight, kids
        return calc_weight


discs = Discs(ins)
print(f"Result 1: {discs.parent(discs.any_kid)}")
try:
    discs.weight()
except TypeError as e:
    print(f"Result 2: {e}")
