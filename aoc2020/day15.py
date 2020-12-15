"""requires python3.8. for f-strings and walrus operator"""
with open("day15.txt") as f_in:
    ins = f_in.read().strip()


def rindex(_list, value):
    try:
        return len(_list) - _list[::-1].index(value) - 1
    except ValueError:
        return None


class Game:
    def __init__(self, text):
        self.data = [int(_) for _ in text.split(",")]
        self.indexes = {
            val: idx for idx, val in enumerate(self.data)
        }

    def __repr__(self):
        return ",".join(map(str, self.data))

    def item(self, index):
        idx = len(self.data)
        while idx != index:
            last = self.data[-1]
            prev_idx = self.indexes.get(last)
            if prev_idx == (idx - 1):
                add = 0
            else:
                add = idx - prev_idx - 1
            prev_idx = rindex(self.data, add)
            self.indexes[add] = idx if prev_idx is None else prev_idx
            self.data.append(add)
            idx += 1

        return self.data[-1]


assert Game("0,3,6").item(2020) == 436
assert Game("1,3,2").item(2020) == 1
game = Game(ins)
print(f"Result 1: {game.item(2020)}")
# assert Game("0,3,6").item(30000000) == 175594
