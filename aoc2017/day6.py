with open("day6.txt") as fin:
    ins = fin.read()

blocks = [int(_) for _ in ins.split()]


def rotate(before):
    memory = before.copy()
    largest = max(*memory)
    working = memory.index(largest)
    dist, memory[working] = memory[working], 0
    for _ in range(dist):
        working += 1
        if working == len(memory):
            working = 0
        memory[working] += 1
    return memory


def balance(memory):
    rotations = 0
    orders = list()
    while memory not in orders:
        orders.append(memory)
        memory = rotate(memory)
        rotations += 1
    return rotations, rotations - orders.index(memory)


rots, cycs = balance(blocks)
print(f"Result 1: {rots}")
print(f"Result 2: {cycs}")
