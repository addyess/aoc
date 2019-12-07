from aoc2019.computer import Machine

with open("day5.txt") as fin:
    ins = fin.read()

machine = Machine.decode(ins, [1])
out = machine.run()
print(f"Result 1: {out[-1]}")

machine = Machine.decode(ins, [5])
out = machine.run()
print(f"Result 2: {out[-1]}")
