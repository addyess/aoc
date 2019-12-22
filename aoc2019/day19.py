try:
    from aoc2019.computer import Machine
except ImportError:
    from computer import Machine
from itertools import count
from collections import deque


def main():
    with open("day19.txt") as fin:
        ins = fin.read()

    counter = 0
    for y in range(0, 50):
        for x in range(0, 50):
            machine = Machine.decode(ins, [x, y])
            machine.run()
            counter += machine.stdout[-1]
    print(f"Result 1: {counter}")

    coords = deque()
    x_start = 0
    sz = 100
    found = None
    for y in count(sz * 10):
        if found:
            break
        xmin, xmax = float('inf'), None
        for x in count(x_start):
            machine = Machine.decode(ins, [x, y])
            machine.run()
            if machine.stdout[-1]:
                xmin, xmax = min(xmin, x), x
            elif not machine.stdout[-1] and xmax is not None:
                break
        x_width = (xmax - xmin + 1)
        x_start = xmin
        if len(coords) == (sz - 1):
            p_min, p_max, p_y, _ = coords.popleft()
            if p_min <= xmin and (xmin + sz - 1) <= p_max:
                found = xmin, p_y
        if x_width >= sz:
            coords += [(xmin, xmax, y, x_width)]
    print(f"Result 2: {found}")


main()
