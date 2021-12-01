#! /usr/bin/python3
import functools

INF = float("inf")

with open("day01.txt") as f_in:
    ins = [int(_.strip()) for _ in f_in]


def win_inc(c, n):
    windows = c[1] + [n]
    increases = c[0] + (sum(windows[:-1]) < sum(windows[1:]))
    return increases, windows[1:]


res1, _ = functools.reduce(win_inc, ins, (False, [INF]))  # window size of 1
print(f"Result 1: {res1}")
res2, _ = functools.reduce(win_inc, ins, (False, [INF] * 3))  # window size of 3
print(f"Result 2: {res2}")
