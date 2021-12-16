with open("day1.txt") as fin:
    ins = [int(_) for _ in fin.read().strip()]


def matches(digits, hops):
    tail = digits
    while tail:
        head, tail = tail[0], tail[1:]
        if head == (tail + digits)[hops]:
            yield head


res1 = sum(matches(ins, 0))
print(f"Result 1: {res1}")

res2 = sum(matches(ins, len(ins) // 2 - 1))
print(f"Result 2: {res2}")
