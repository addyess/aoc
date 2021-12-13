from itertools import product, count


class Octopi:
    def __init__(self, lines):
        self.init = {
            (x, y): int(height)
            for x, line in enumerate(lines)
            for y, height in enumerate(line.strip())
        }
        self.map = dict(self.init.items())

    def adjacent(self, pos):
        pos_x, pos_y = pos
        for x, y in product(range(-1, 2), repeat=2):
            new_pos = pos_x + x, pos_y + y
            if new_pos in self.map:
                yield new_pos

    def step(self):
        next_map = {k: v + 1 for k, v in self.map.items()}  # increase everyone by 1
        new_flashers = flashers = {k for k, v in next_map.items() if v >= 10}
        while new_flashers:
            for loc in new_flashers:
                for adj in self.adjacent(loc):
                    next_map[adj] += 1
            new_flashers = {k for k, v in next_map.items() if v >= 10} - flashers
            flashers |= new_flashers
        self.map = {
            k: 0 if v > 9 else v for k, v in next_map.items()
        }  # reset any who flashed
        return len(flashers)

    def reset(self):
        self.map = dict(self.init.items())


with open("day11.txt") as fin:
    octopi = Octopi(fin)

res1 = 0
for _ in range(0, 100):
    res1 += octopi.step()
print(f"Result 1: {res1}")
octopi.reset()

for res2 in count(1):
    if octopi.step() == len(octopi.map):
        print(f"Result 2: {res2}")
        break
