from aoc2019.computer import Machine
with open("day9.txt") as fin:
    ins = fin.read().strip()

mach = Machine.decode(ins, [1])
out = mach.run()
print(f"Result 1: {out}")

mach = Machine.decode(ins, [2])
out = mach.run()
print(f"Result 2: {out}")
