from itertools import takewhile
from collections import defaultdict
from math import prod

with open("day16.txt") as f_in:
    ins = [_.strip() for _ in f_in]


def mkrule(text):
    title, validation = text.split(": ")
    l, r = validation.split(" or ")
    ranges = (
        [int(_) for _ in l.split("-")],
        [int(_) for _ in r.split("-")]
    )
    return title, (
        list(range(ranges[0][0], ranges[0][1] + 1)),
        list(range(ranges[1][0], ranges[1][1] + 1))
    )


class Tickets:
    @classmethod
    def parse(cls, lines):
        it = iter(lines)
        rules = list(takewhile(lambda l: l, it))
        my_ticket = list(takewhile(lambda l: l, it))
        near_tickets = list(takewhile(lambda l: l, it))
        return cls(rules, my_ticket[1:], near_tickets[1:])

    def __init__(self, rules, mine, theirs):
        self.rules = dict(mkrule(text) for text in rules)
        self.mine = [int(_) for _ in mine[0].split(',')]
        self.theirs = [
            [int(_) for _ in a_ticket.split(',')]
            for a_ticket in theirs
        ]
        self.index_map = {
            k: set(range(0, len(self.mine)))
            for k in self.rules.keys()
        }

    def valid_one_place(self, value):
        for left, right in self.rules.values():
            if value in left or value in right:
                return value
        return None

    def error_rate(self):
        for scanned in self.theirs:
            for value in scanned:
                if not self.valid_one_place(value):
                    yield value

    def valid_ticket(self, scanned):
        for value in scanned:
            if not self.valid_one_place(value):
                return None
        return scanned

    @property
    def valid_scans(self):
        for scanned in self.theirs:
            if self.valid_ticket(scanned):
                yield scanned

    def isolate_fields(self):
        for scanned in self.valid_scans:
            if all(len(_) == 1 for _ in self.index_map.values()):
                return
            new_map = defaultdict(set)
            for rule, possible in self.index_map.items():
                if len(possible) == 1:
                    new_map[rule] = possible
                    continue
                left, right = self.rules[rule]
                for idx in possible:
                    if scanned[idx] in left or scanned[idx] in right:
                        new_map[rule].add(idx)
            self.index_map = reduce(new_map)


def reduce(index_map):
    working = index_map
    first = True
    while first or working != index_map:
        first = False
        index_map = {k: set(v) for k, v in working.items()}
        for k, v, in index_map.items():
            if len(v) == 1:
                working = {kw: vw - v for kw, vw in working.items()}
                working[k] = v
    return working


tickets = Tickets.parse(ins)
print(f"Result 1: {sum(tickets.error_rate())}")
tickets.isolate_fields()
product = prod(
    tickets.mine[next(iter(idx))]
    for rule, idx in tickets.index_map.items()
    if rule.startswith('departure')
)
print(f"Result 2: {product}")
