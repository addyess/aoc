import re
from collections import UserDict

TITLE_RE = re.compile(r"^(\S+ \S+) bags contain")
CONTAINS_RE = re.compile(r"(\d+) (\S+ \S+) bags?")

with open("day07.txt") as f_in:
    ins = [_.strip() for _ in f_in]


class Rule(UserDict):
    rules = {}

    @classmethod
    def parsed(cls, stream):
        def record(_):
            outer_bag, = TITLE_RE.search(_).groups()
            return outer_bag, cls({
                inner_bag: int(num)
                for num, inner_bag in CONTAINS_RE.findall(_)
            })

        return dict(record(line) for line in stream)

    def can_contain(self, bag):
        if bag in self.data:
            return True
        for content in self.data.keys():
            if self.rules.get(content).can_contain(bag):
                return True
        return False

    def count_nested(self, count_self=False):
        return sum(
            mul * self.rules[bag].count_nested(True)
            for bag, mul in self.data.items()
        ) + count_self


Rule.rules = Rule.parsed(ins)
res1 = sum(_.can_contain("shiny gold") for _ in Rule.rules.values())
print(f"Result 1: {res1}")
res2 = Rule.rules['shiny gold'].count_nested()
print(f"Result 2: {res2}")
