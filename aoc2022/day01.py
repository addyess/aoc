#! /usr/bin/python3
from aoc.file import puzzle_input


def elf_calories():
    current_elf = []
    for line in puzzle_input():
        if line.strip() == "":
            yield sum(current_elf)
            current_elf = []
        else:
            current_elf.append(int(line))
    yield sum(current_elf)


res1 = sorted(list(elf_calories()), reverse=True)
print(f"Result 1: {res1[0]}")
print(f"Result 2: {sum(res1[:3])}")
