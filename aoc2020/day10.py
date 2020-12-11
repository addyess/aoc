from collections import defaultdict
with open("day10.txt") as f_in:
    ins = sorted([int(_.strip()) for _ in f_in])


def find_simple_joltage_chain(it):
    it = it + [it[-1] + 3]
    prev, buckets = 0, defaultdict(int)
    for j in it:
        buckets[j-prev] += 1
        prev = j
    return buckets[1] * buckets[3]


def calculate_combinations(it):
    """
    Shameless cheating
    https://www.reddit.com/r/adventofcode/comments/ka9pc3/2020_day_10_part_2_suspicious_factorisation/
    """
    full = [0] + it + [it[-1] + 3]
    pow2, pow7 = 0, 0
    for i in range(1, len(full)-1):
        neg3 = full[i-3] if (i >= 3) else -9999
        if full[i+1] - neg3 == 4:
            pow7 += 1
            pow2 -= 2
        elif full[i+1] - full[i-1] == 2:
            pow2 += 1
    return pow(2, pow2) * pow(7, pow7)


res1 = find_simple_joltage_chain(ins)
print(f"Result 1: {res1}")
res2 = calculate_combinations(ins)
print(f"Result 2: {res2}")
