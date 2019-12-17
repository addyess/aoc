from itertools import cycle, repeat
try:
    from blist import blist
except ImportError:
    blist = list


def repeated(it, times):
    skip = True
    for elem in cycle(it):
        for rep in repeat(elem, times):
            if skip:
                skip = False
                continue
            yield rep


def dot(it1, it2):
    return blist(a * b for a, b in zip(it1, it2))


def phase(nums):
    half = len(nums)//2
    for idx in range(len(nums)):
        s = nums[idx:] if idx >= half else dot(nums, repeated([0, 1, 0, -1], idx + 1))
        yield abs(sum(s)) % 10


def fft(nums, phases):
    for idx in range(phases):
        nums = blist(phase(nums))
    return nums


def lazy_fft(nums, phases):
    for idx in range(phases):
        running = 0
        next_nums = []
        for end in reversed(nums):
            running += end
            running = running % 10
            next_nums.append(running)
        nums = blist(reversed(next_nums))
    return nums


def collapse(seq):
    return sum((10 ** idx) * num for idx, num in enumerate(reversed(seq)))


def main():
    with open("day16.txt") as fin:
        ins = fin.read()

    nums = [int(_) for _ in ins]
    out = fft(nums, 100)
    print(f"Result 1: {collapse(out[:8])}")

    nums = [int(_) for _ in ins]
    offset = collapse(nums[:7])
    assert offset > len(nums) * 5000
    real_in = blist(nums * 10000)
    out = lazy_fft(real_in[offset:], 100)
    print(f"Result 2: {collapse(out[:8])}")


main()
