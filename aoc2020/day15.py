"""requires python3.8. for f-strings and walrus operator"""
with open("day15.txt") as f_in:
    ins = f_in.read().strip()


class Game:
    def __init__(self, text):
        data = [int(_) for _ in text.split(",")]
        # Record the previous indexes -- except for the last element
        # evaluated the last element
        self.indexes = {val: idx for idx, val in enumerate(data[:-1])}
        self.start = data[-1], len(data)

    def item(self, index):
        last, idx = self.start
        while idx != index:
            prev, self.indexes[last] = self.indexes.get(last), idx - 1
            last = 0 if prev is None else (idx - prev - 1)
            idx += 1
        return last


print(f"Result 1: {Game(ins).item(2020)}")
print(f"Result 2: {Game(ins).item(30000000)}")
