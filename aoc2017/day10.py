from functools import reduce
from itertools import islice

with open("day10.txt") as fin:
    ins = fin.read().strip()


def as_ints():
    return list(map(int, ins.split(",")))


def as_ascii():
    for s in ins:
        yield ord(s)
    for s in [17, 31, 73, 47, 23]:
        yield s


def as_dense(sparse):
    it = iter(sparse)
    for _ in range(0, 16):
        yield reduce(lambda a, v: a ^ v, islice(it, 16), 0)


def as_hex(seq):
    return "".join("{:x}".format(_) for _ in seq)


def knot_hash(nums, _seq, i=0, skip=0):
    init = len(nums)
    for length in _seq:
        _nums = nums + nums
        revd = list((_nums[i : i + length]))[::-1]
        for o, v in enumerate(revd):
            nums[(i + o) % init] = v
        i = (i + length + skip) % init
        skip += 1
    return nums, i, skip


def main():
    nums = list(range(0, 256))
    result, _, _ = knot_hash(nums, as_ints())
    print(f"Result 1: {result[0] * result[1]}")

    sparse = list(range(0, 256))
    i, skip = 0, 0
    for _ in range(0, 64):
        sparse, i, skip = knot_hash(sparse, as_ascii(), i, skip)
    dense = as_dense(sparse)
    print(f"Result 2: {as_hex(dense)}")


main()
