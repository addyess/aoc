from aoc2019.computer import Machine

with open("day2.txt") as fin:
    ins = fin.read()


machine = Machine.decode(ins)
# 1202 error0
machine.locs[1], machine.locs[2] = 12, 2
machine.run()
print(f"Result 1: {machine.locs[0]}")

search = 19690720
for noun in range(100):
    for verb in range(100):
        machine = Machine.decode(ins)
        machine.locs[1] = noun
        machine.locs[2] = verb
        machine.run()
        if machine.locs[0] == search:
            print(f"Result 2: {(noun * 100 + verb)}")
