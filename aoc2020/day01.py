#! /usr/bin/python3.7
import math

with open("day01.txt") as f_in:
    ins = [int(_.strip()) for _ in f_in.readlines()]


def find_n_addends(n, series, expected=2020):
    """
    Find N integers in a series that sum to the expected value.
    :param  int n: number of elements to sum
    :param  list series: list of elements
    :param  int expected: value to sum to
    :returns n-tuple of 0s if not found, otherwise n-tuple of the matches
    """
    if n == 1:
        return (expected,) if expected in series else (0,)
    for cur, i in enumerate(series):
        res = find_n_addends(n-1, series[cur+1:], expected - i)
        if not all(_ == 0 for _ in res):
            return (i,) + res
    return (0,) * n


res1 = find_n_addends(2, ins)
print(f"Result 1: {math.prod(res1)}")
res2 = find_n_addends(3, ins)
print(f"Result 2: {math.prod(res2)}")
