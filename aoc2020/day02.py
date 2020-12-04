#! /usr/bin/python3


def parse(entry):
    policy, req, password = entry.split()
    lo, hi = map(int, policy.split("-"))
    return lo, hi, req.strip(":"), password


with open("day02.txt") as f_in:
    ins = [parse(_) for _ in f_in]


def is_valid_old_shop(entry):
    lo, hi, req, p = entry
    return lo <= p.count(req) <= hi


def is_valid_new_shop(entry):
    lo, hi, req, p = entry
    return [p[lo-1], p[hi-1]].count(req) == 1


res1 = sum(map(is_valid_old_shop, ins))
print(f"Result 1: {res1}")
res2 = sum(map(is_valid_new_shop, ins))
print(f"Result 2: {res2}")
