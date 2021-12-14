from collections import Counter


class Polymer:
    def __init__(self, lines):
        template = lines[0]
        lines = lines[2:]
        self.pair_frequencies = Counter(zip(template, template[1:]))
        self.char_frequencies = Counter(template)
        self.rules = {tuple(p): v for p, v in (line.split(" -> ") for line in lines)}

    def step(self, steps):
        for _ in range(steps):
            pair_frequencies_step = Counter()
            for (x, y), frequency in self.pair_frequencies.items():
                pair_frequencies_step[x, self.rules[(x, y)]] += frequency
                pair_frequencies_step[self.rules[(x, y)], y] += frequency
                self.char_frequencies[self.rules[(x, y)]] += frequency
            self.pair_frequencies = pair_frequencies_step

        return max(self.char_frequencies.values()) - min(self.char_frequencies.values())


with open("day14.txt") as fin:
    ins = fin.read().splitlines()

polymer = Polymer(ins)
print(f"Result 1: {polymer.step(10)}")
print(f"Result 2: {polymer.step(30)}")
