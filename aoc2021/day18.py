import math
from collections import namedtuple
from functools import reduce, cached_property
from itertools import permutations


class Value(namedtuple("Value", "magnitude")):
    def __repr__(self):
        return str(self.magnitude)


class Pair:
    @classmethod
    def parse(cls, arg):
        if isinstance(arg, list):
            return [cls.parse(line) for line in arg]
        if isinstance(arg, str):
            return cls(cls.unfold(eval(arg.strip())))

    def __init__(self, as_list):
        self.unfolded = as_list

    def __repr__(self):
        return f"[{self.left}, {self.right}]"

    @property
    def magnitude(self):
        return (self.left.magnitude * 3) + (self.right.magnitude * 2)

    @cached_property
    def mid(self):
        cur = 0
        for idx, (_, depth) in enumerate(self.unfolded):
            cur += 1 / (2 ** depth)
            if cur > 1:
                return idx

    @property
    def left(self):
        return self.fold(self.unfolded[: self.mid])

    @property
    def right(self):
        return self.fold(self.unfolded[self.mid :])

    @classmethod
    def fold(cls, half):
        if len(half) == 1:
            return Value(half[0][0])
        return cls([(v, depth - 1) for (v, depth) in half])

    @classmethod
    def unfold(cls, l_arg=None, depth=-1):
        if isinstance(l_arg, list):
            return [__ for _ in l_arg for __ in cls.unfold(_, depth + 1)]
        return [(l_arg, depth)]

    def __add__(self, other):
        return Pair(
            [(v, depth + 1) for v, depth in self.unfolded + other.unfolded]
        ).reduce()

    def reduce(self):
        p, changed = self.explode()
        if changed:
            p = p.reduce()
        p, changed = p.split()
        if changed:
            p = p.reduce()
        return p

    def explode(self):
        unfolded = dict(enumerate(self.unfolded))
        updated = []
        for idx, (v, depth) in unfolded.items():
            if depth < 4:
                updated.append((v, depth))
            else:
                adder = unfolded.get(idx - 1)
                if adder:
                    v = v + adder[0]
                    updated[-1] = (v, adder[1])

                updated.append((0, depth - 1))

                adder = unfolded.get(idx + 2)
                if adder:
                    v, depth = unfolded.get(idx + 1)
                    v = v + adder[0]
                    updated.append((v, adder[1]))
                updated += self.unfolded[idx + 3 :]
                break

        return Pair(updated), self.unfolded != updated

    def split(self):
        updated = []
        for idx, (v, depth) in enumerate(self.unfolded):
            if v > 9:
                updated.append((math.floor(v / 2), depth + 1))
                updated.append((math.ceil(v / 2), depth + 1))
                updated += self.unfolded[idx + 1 :]
                break
            else:
                updated.append((v, depth))
        return Pair(updated), self.unfolded != updated


with open("day18.txt") as fin:
    h = Pair.parse(fin.readlines())
reduced = reduce(Pair.__add__, h)
print(f"Result 1 {reduced.magnitude}")
m = max((x + y).magnitude for x, y in permutations(h, 2))
print(f"Result 2 {m}")
