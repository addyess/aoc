#! /usr/bin/python3
import statistics


class Crabs:
    @classmethod
    def parse(cls, line):
        return cls([int(_) for _ in line.split(",")])

    def __init__(self, initial):
        self.initial = initial
        # Part 1
        self.median = round(statistics.median(self.initial), None)
        self.fuel_to_median = min(
            sum(abs(x - center) for x in self.initial)
            for center in (self.median + x for x in range(-1, 2))
        )

        # Part 2
        def fuel_by_dist(dist):
            return sum(range(1, dist)) + dist

        self.mean = round(statistics.mean(self.initial), None)
        self.fuel_to_mean = min(
            sum(fuel_by_dist(abs(x - center)) for x in self.initial)
            for center in (self.mean + x for x in range(-1, 2))
        )


with open("day07.txt") as fin:
    ins = fin.read()
crabs = Crabs.parse(ins)

print(f"Result 1: {crabs.fuel_to_median}")
print(f"Result 2: {crabs.fuel_to_mean}")
