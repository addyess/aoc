import re
from collections import defaultdict

with open("day8.txt") as fin:
    instructions = fin.readlines()

regs = defaultdict(int)
highest = -float("inf")
ins_re = re.compile(r"(\S+) ((?:inc)|(?:dec)) (-*\d+) if (\S+) (\S+) (-*\d+)")
for ins in instructions:
    reg, op, val, c_reg, c_op, c_val = ins_re.match(ins).groups()
    if eval(f"{regs[c_reg]} {c_op} {c_val}"):
        regs[reg] += int(val) if op == "inc" else (0 - int(val))
        highest = max(regs[reg], highest)

print(f"Result 1: {max(regs.values())}")
print(f"Result 2: {highest}")
