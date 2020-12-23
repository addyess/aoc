from itertools import chain


class Cups:
    def __init__(self, init, max_num=None):
        self.max = max_num or len(cup_labels)
        self.graph = {}
        self.cur = p = init[0]
        for label in chain(init[1:], range(10, self.max+1)):
            self.graph[p] = label
            p = label
        self.graph[p] = self.cur

    @property
    def part1(self):
        n = self.graph[1]
        p1 = ""
        while len(p1) < self.max-1:
            p1 += str(n)
            n = self.graph[n]
        return p1

    @property
    def part2(self):
        n1 = self.graph[1]
        n2 = self.graph[n1]
        return n1 * n2

    def move(self):
        # Remove Cups
        remove = []
        n = self.graph[self.cur]
        for _ in range(3):
            remove.append(n)
            n = self.graph[n]
        self.graph[self.cur] = n

        # Select Destination Label
        dest = self.cur - 1
        while dest == 0 or dest in remove:
            if dest == 0:
                dest = self.max
            else:
                dest -= 1

        # Insertion
        pos, self.graph[dest] = self.graph[dest], remove[0]
        self.graph[remove[-1]] = pos

        # Setup Next
        self.cur = self.graph[self.cur]


ins = "496138527"
cup_labels = list(map(int, ins))
cups = Cups(cup_labels)
for _ in range(100):
    cups.move()
print(f"Result 1: {cups.part1}")

cups = Cups(cup_labels, 1000000)
for _ in range(10000000):
    cups.move()
print(f"Result 2: {cups.part2}")
