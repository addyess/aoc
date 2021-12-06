#! /usr/bin/python3
from functools import reduce


def parse(line):
    command, scalar = line.split()
    return command, int(scalar)


def navigate(loc, cur):
    inst, value = cur
    if inst == "forward":
        loc[0] += value
    elif inst == "down":
        loc[1] += value
    else:
        loc[1] -= value
    return loc


def navigate_by_aim(acc, cur):
    inst, value = cur
    loc, aim = acc
    if inst == "forward":
        loc[0] += value
        loc[1] += aim * value
    elif inst == "down":
        aim += value
    else:
        aim -= value
    return loc, aim


with open("day02.txt") as f_in:
    ins = list(map(parse, f_in))

end = reduce(navigate, ins, [0, 0])
print(f"Result 1: {end[0]*end[1]}")

end, _ = reduce(navigate_by_aim, ins, ([0, 0], 0))
print(f"Result 2: {end[0]*end[1]}")
