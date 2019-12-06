from aoc2019.computer import Machine

with open("day5.txt") as fin:
    ins = fin.read()

machine = Machine.decode(ins)
out = machine.run([1])
print(f"Result 1: {out[-1]}")

machine = Machine.decode(ins)
out = machine.run([5])
print(f"Result 2: {out[-1]}")
