"""requires python3.8. for f-strings and walrus operator"""
with open("day15.txt") as f_in:
    ins = f_in.read().strip()


class Game:
    def __init__(self, text):
        self.data = [int(_) for _ in text.split(",")]
        # Record the previous indexes -- except for the last element
        # We've not evaluated the last element yet
        self.indexes = {
            val: idx for idx, val in enumerate(self.data[:-1])
        }

    def item(self, index):
        idx = len(self.data)
        while idx != index:
            this = self.data[-1]
            prev, self.indexes[this] = self.indexes.get(this), idx - 1
            add = 0 if prev is None else (idx - prev - 1)
            self.data.append(add)
            idx += 1

        return self.data[-1]


game = Game(ins)
print(f"Result 1: {game.item(2020)}")
print(f"Result 2: {game.item(30000000)}")
