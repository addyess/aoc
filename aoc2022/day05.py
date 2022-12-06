#! /usr/bin/python3
from aoc.file import example, puzzle_input
from collections import defaultdict, namedtuple
import re

Move = namedtuple("Move", "count, src, dst")
EX_TEXT = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""


def stack_lines(lines):
    stacks = []
    for line in lines:
        if line.strip() == "":
            break
        stacks.append(line)
    return stacks


def parse_stacks(stacks):
    match_re = re.compile(r"\[(\S)\]")
    ids = [id for id in stacks[0] if id != " "]
    part = len(stacks[0]) // len(ids) + 1
    stack = {name: [] for name in ids}

    for row in stacks[1:]:
        for i, name in enumerate(ids):
            crate = row[i * part : (i + 1) * part]
            if m := match_re.match(crate):
                stack[name].extend(m.groups())
    return stack


def parse_moves(moves):
    move_re = re.compile(r"move (\d+) from (\S) to (\S)")
    for row in moves:
        num, src, dst = move_re.findall(row)[0]
        yield Move(int(num), src, dst)


def cm_9000(stacks, moves):
    stacks = {k: s.copy() for k, s in stacks.items()}
    for move in moves:
        for _ in range(move.count):
            stacks[move.dst].append(stacks[move.src].pop())
    return "".join(stack[-1] for stack in stacks.values())


def cm_9001(stacks, moves):
    stacks = {k: s.copy() for k, s in stacks.items()}
    for move in moves:
        top = stacks[move.src][0 - move.count :]
        stacks[move.src] = stacks[move.src][: 0 - move.count]
        stacks[move.dst].extend(top)
    return "".join(stack[-1] for stack in stacks.values())


def solver(lines):
    stacks = parse_stacks(stack_lines(lines)[::-1])
    moves = list(parse_moves(lines))
    return cm_9000(stacks, moves), cm_9001(stacks, moves)


assert ("CMZ", "MCD") == solver(example(EX_TEXT))

res1, res2 = solver(puzzle_input())
print(f"Result 1: {res1}")
print(f"Result 2: {res2}")
