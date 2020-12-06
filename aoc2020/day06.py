from aoc2020.utils import GroupParsed
from functools import reduce

with open("day06.txt") as f_in:
    ins = [_.strip() for _ in f_in]


class Response(GroupParsed):
    def __init__(self, group):
        self.group = group

    @property
    def num_any_yes(self):
        return len(set("".join(self.group)))

    @property
    def num_all_yes(self):
        all_yes = [set(_) for _ in self.group]
        return len(reduce(lambda acc, elem: acc & elem, all_yes))


answers = list(Response.parsed(ins))
print(f"Result 1: {sum(_.num_any_yes for _ in answers)}")
print(f"Result 2: {sum(_.num_all_yes for _ in answers)}")
