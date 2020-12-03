from itertools import count
from math import prod

with open("day03.txt") as f_in:
    ins = [_.strip() for _ in f_in.readlines()]


def trees_encountered(forest, r, d):
    """
    How many trees do you encounter sliding through this forest?
    :param List[str] forest: map of the forest
    :param r: x-part of the slope
    :param d: y-part of the slope
    :return: count of trees encountered on this slope
    """
    return sum(
        row[x % len(row)] == "#"
        for row, x in zip(forest[::d], count(step=r))
    )


res1 = trees_encountered(ins, 3, 1)
print(f"Result 1: {res1}")

res2 = (
    trees_encountered(ins, 1, 1),
    res1,
    trees_encountered(ins, 5, 1),
    trees_encountered(ins, 7, 1),
    trees_encountered(ins, 1, 2),
)
print(f"Result 2: {prod(res2)}")
