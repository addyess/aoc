#! /usr/bin/python3.7

with open("day1.txt") as f_in:
    ins = [int(_.strip()) for _ in f_in.readlines()]


def fuel_req(mod, plus_fuel=False):
    fuel = max((mod // 3) - 2, 0)
    if plus_fuel and fuel:
        fuel += fuel_req(fuel, plus_fuel)
    return fuel


res1 = sum(fuel_req(_) for _ in ins)
print(f"Result 1 {res1}")
res2 = sum(fuel_req(_, True) for _ in ins)
print(f"Result 2 {res2}")
