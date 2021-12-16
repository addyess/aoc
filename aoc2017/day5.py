with open("day5.txt") as fin:
    ins = fin.readlines()


def trampoline(jumps, rule):
    steps, pc = 0, 0
    while True:
        try:
            npc = jumps[pc]
            jumps[pc] = npc + rule(npc)
            pc += npc
            steps += 1
        except IndexError:
            return steps


print(f"Result 1: {trampoline([int(_) for _ in ins], lambda _: 1)}")
print(f"Result 2: {trampoline([int(_) for _ in ins], lambda o: -1 if o > 2 else 1)}")
