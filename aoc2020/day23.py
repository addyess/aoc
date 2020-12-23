from itertools import count

VERBOSE = True
ins = "496138527"
# ins = "389125467"
cup_labels = list(ins)


def verbose(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)


class Cups:
    def __init__(self, start):
        self.buckets = [int(_) for _ in start]
        self.max = max(self.buckets)
        self.cur = 0
        self.cur_move = 0

    def __str__(self):
        repr = (
            self.buckets[0:self.cur] +
            [f'({self.buckets[self.cur]})'] +
            self.buckets[self.cur+1:]
        )
        return ' '.join(map(str, repr))

    def next_cur(self, cur):
        cur += 1
        return cur % len(self.buckets)

    @property
    def final(self):
        cur = self.buckets.index(1)
        return "".join(
            str(self.buckets[self.next_cur(cur + _)])
            for _ in range(len(self.buckets)-1)
        )

    def move(self):
        # Select to Remove
        self.cur_move += 1
        verbose(f"-- move {self.cur_move}-- ")
        verbose(f"cups: {self}")

        # Remove Cups
        next3 = [self.next_cur(self.cur + _) for _ in range(3)]
        next3_label = [self.buckets[_] for _ in next3]
        for r in next3:
            self.buckets[r] = None
        verbose(f"pickup: {', '.join(map(str, next3_label))}")

        # Select Destination Label
        dest = self.buckets[self.cur] - 1
        while dest in next3_label or dest == 0:
            if dest == 0:
                dest = self.max
            else:
                dest -= 1
        verbose(f"destination: {dest}")
        verbose()

        # Insertion
        label_cur = self.buckets[self.cur]
        pos = self.buckets.index(dest) + 1
        for p in reversed(next3_label):
            self.buckets.insert(pos, p)

        # Flatten
        self.buckets = [_ for _ in self.buckets if _ is not None]
        self.cur = self.next_cur(self.buckets.index(label_cur))


cups = Cups(cup_labels)
for _ in range(100):
    cups.move()
print(f"Result 1: {cups.final}")
