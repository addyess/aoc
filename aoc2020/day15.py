"""requires python3.8. for f-strings and walrus operator"""
with open("day15.txt") as f_in:
    ins = f_in.read().strip()


class Game:
    def __init__(self, text):
        self.data = [int(_) for _ in text.split(",")]
        self.indexes = {
            val: idx for idx, val in enumerate(self.data[:-1])
        }

    def item(self, index):
        idx = len(self.data)
        while idx != index:
            last = self.data[-1]
            prev_idx, self.indexes[last] = self.indexes.get(last), idx - 1
            if prev_idx is None:
                add = 0
            else:
                add = idx - prev_idx - 1
            self.data.append(add)
            idx += 1

        return self.data[-1]


game = Game(ins)
print(f"Result 1: {game.item(2020)}")
print(f"Result 2: {game.item(30000000)}")
