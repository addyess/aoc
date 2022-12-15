#! /usr/bin/python3
from aoc.file import puzzle_input, example

EX_TEXT = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""

dir = {
    "U": (0, 1),
    "D": (0, -1),
    "L": (-1, 0),
    "R": (1, 0),
}


def parse(lines):
    return [(k, int(v)) for k, v in ((line.split(" ") for line in lines))]


def add(a, b):
    return tuple(map(sum, zip(a, b)))


def touch(a, b):
    return any(add(a, (x, y)) == b for x in range(-1, 2) for y in range(-1, 2))


def move_toward(a, b):
    if a[0] == b[0]:  # vertically separated
        return b[0], (a[1] + b[1]) // 2
    elif a[1] == b[1]:  # horizontally separated
        return (a[0] + b[0]) // 2, b[1]
    elif abs(a[0] - b[0]) == 1:  # vertically diagonal
        return b[0], (a[1] + b[1]) // 2
    elif abs(a[1] - b[1]) == 1:  # horizontally diagonal
        return (a[0] + b[0]) // 2, b[1]
    return (a[0] + b[0]) // 2, (a[1] + b[1]) // 2


def count_tail_moves(moves, space):
    t = len(space) - 1
    tail_moves = {space[t]}
    for move in moves:
        for turns in range(move[1]):
            space[0] = add(space[0], dir[move[0]])
            for knot in range(t):
                if not touch(space[knot + 1], space[knot]):
                    space[knot + 1] = move_toward(space[knot + 1], space[knot])
            tail_moves.add(space[t])
    return len(tail_moves)


def solver(lines):
    head_directions = parse(lines)

    space = {i: (0, 0) for i in range(2)}
    two_knots = count_tail_moves(head_directions, space)

    space = {i: (0, 0) for i in range(10)}
    ten_knots = count_tail_moves(head_directions, space)

    return two_knots, ten_knots


res1, res2 = solver(example(EX_TEXT))
assert (res1, res2) == (88, 36)
res1, res2 = solver(puzzle_input())
print(f"Result 1: {res1}")
print(f"Result 2: {res2}")
