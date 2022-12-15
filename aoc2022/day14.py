#! /usr/bin/python3
from aoc.file import example, puzzle_input
from itertools import pairwise


EX_TEXT = """\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""


def parser(lines):
    grid = {}
    for line in lines:
        coords = (
            tuple(map(int, coord.split(",")))
            for coord in map(str.strip, line.split("->"))
        )
        for s, e in pairwise(coords):
            if s[0] == e[0]:
                yr = (s[1], e[1])
                grid.update({(s[0], y): "#" for y in range(min(yr), max(yr) + 1)})
            else:
                xr = (s[0], e[0])
                grid.update({(x, s[1]): "#" for x in range(min(xr), max(xr) + 1)})
    return grid


def grid_edges(grid, dim):
    return min(loc[dim] for loc in grid) - 1, max(loc[dim] for loc in grid) + 1


def drop(grid, edges, loc):
    x, y = loc
    while x not in edges[0] and y not in edges[1]:
        down = x, y + 1
        left = x - 1, y + 1
        right = x + 1, y + 1
        if not grid.get(down):
            loc = down
        elif not grid.get(left):
            loc = left
        elif not grid.get(right):
            loc = right
        else:
            break
        x, y = loc
    return None if x in edges[0] or y in edges[1] else loc


def fill(grid, sand):
    grid.update({sand: "+"})
    edges = grid_edges(grid, 0), grid_edges(grid, 1)
    count = 0
    while loc := drop(grid, edges, sand):
        grid[loc] = "o"
        count += 1
        if loc == sand:
            break
    return count


def solver(lines):
    sparse_grid = parser(lines)
    p1 = fill(sparse_grid.copy(), (500, 0))

    x_min, x_max = grid_edges(sparse_grid, 0)
    _, y_max = grid_edges(sparse_grid, 1)

    sparse_grid.update(
        {(x, y_max + 1): "#" for x in range(x_min - y_max, x_max + y_max + 1)}
    )
    p2 = fill(sparse_grid.copy(), (500, 0))
    return p1, p2


print("Puzzle Example")
res1, res2 = solver(example(EX_TEXT))
assert (res1, res2) == (24, 93)
print("Puzzle Input")
res1, res2 = solver(puzzle_input())
print(f"Result 1: {res1}")
print(f"Result 2: {res2}")
