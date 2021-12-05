#! /usr/bin/python3
from functools import reduce, cached_property
from itertools import zip_longest
from dataclasses import dataclass


with open("day03.txt") as f_in:
    ins = list(f_in)


def as_bin(s):
    return int(s, 2) if not isinstance(s, int) else s


@dataclass
class SubStats:
    raw: list[str]

    @property
    def bit_length(self):
        return len(self.raw[0].strip())

    def bit_sum(self, sums, line):
        cur_set, cur = [], as_bin(line)
        for b in range(self.bit_length):
            cur_set.append(1 if (cur >> b) & 1 else -1)
        return list(map(lambda t: t[0] + t[1], zip_longest(sums, cur_set, fillvalue=0)))

    def find_commonality(self, num_set):
        return reduce(self.bit_sum, num_set, list())

    @cached_property
    def gamma_epsilon(self):
        gamma, epsilon = 0, 0
        counts = self.find_commonality(self.raw)
        for b, bit_sum in enumerate(counts):
            gamma |= (1 << b) if bit_sum > 0 else 0
            epsilon |= (1 << b) if bit_sum < 0 else 0
        return gamma, epsilon

    def ratings(self, matcher):
        final = list(map(as_bin, self.raw))
        for b in reversed(range(self.bit_length)):
            val = self.find_commonality(final)[b]
            if matcher(val):
                final = [_ for _ in final if (_ & 1 << b) != 0]
            else:
                final = [_ for _ in final if (_ & 1 << b) == 0]
            if len(final) == 1:
                return final[0]
        return None

    @property
    def gamma(self):
        return self.gamma_epsilon[0]

    @property
    def epsilon(self):
        return self.gamma_epsilon[1]

    @cached_property
    def o_ratings(self):
        return self.ratings(lambda v: v >= 0)

    @cached_property
    def co2_ratings(self):
        return self.ratings(lambda v: v < 0)


stats = SubStats(ins)
res1 = stats.gamma * stats.epsilon
print(f"Result 1: {res1}")
res2 = stats.o_ratings * stats.co2_ratings
print(f"Result 2: {res2}")
