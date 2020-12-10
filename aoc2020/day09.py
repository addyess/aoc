from itertools import combinations

with open("day09.txt") as f_in:
    ins = [int(_.strip()) for _ in f_in]
    base_preamble = 25


def not_xmas_seq(series, preamble):
    for idx, value in enumerate(series):
        if idx < preamble:
            continue
        if any(
            sum(comb) == value
            for comb in combinations(series[idx - preamble:idx], 2)
        ):
            continue
        return idx, value


def contiguous_block(series, invalid):
    for sz in range(2, len(series)):
        for i in range(len(series) - sz + 1):
            seq = series[i:sz+i]
            if sum(seq) == invalid:
                return min(seq), max(seq)


pos, res1 = not_xmas_seq(ins, base_preamble)
print(f"Result 1: {res1}")
small, large = contiguous_block(ins[:pos], res1)
print(f"Result 2: {small+large}")
