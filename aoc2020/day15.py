with open("day15.txt") as f_in:
    ins = f_in.read().strip()


def game(text, index):
    data = [int(_) for _ in text.split(",")]
    # Record the previous indexes -- except for the last element
    indexes = {val: idx for idx, val in enumerate(data[:-1])}
    last = data[-1]
    for idx in range(len(data), index):
        prev, indexes[last] = indexes.get(last), idx - 1
        last = 0 if (prev is None) else (idx - 1 - prev)
    return last


print(f"Result 1: {game(ins,2020)}")
print(f"Result 2: {game(ins,30000000)}")
