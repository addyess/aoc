"""requires python3.8. for f-strings and walrus operator"""
with open("day15.txt") as f_in:
    ins = f_in.read().strip()


def game(text, index):
    data = [int(_) for _ in text.split(",")]
    # Record the previous indexes -- except for the last element
    indexes = {val: idx for idx, val in enumerate(data[:-1])}
    last, idx = data[-1], len(data)
    while idx != index:
        prev, indexes[last] = indexes.get(last), idx - 1
        last = 0 if prev is None else (idx - prev - 1)
        idx += 1
    return last


print(f"Result 1: {game(ins,2020)}")
print(f"Result 2: {game(ins,30000000)}")
