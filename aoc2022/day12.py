#! /usr/bin/python3
from aoc.file import example, puzzle_input
from dijkstra import Graph, DijkstraSPF
from tqdm import tqdm


EX_TEXT = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""


def neighbors(node, x_range: int, y_range: int):
    x, y = node
    if x > 0:
        yield (x - 1, y)  # LEFT
    if x < x_range:
        yield (x + 1, y)  # RIGHT
    if y > 0:
        yield (x, y - 1)  # UP
    if y < y_range:
        yield (x, y + 1)  # DOWN


def distance(current, neighbor, points):
    elevation_climb = ord(points[neighbor]) - ord(points[current])
    return elevation_climb <= 1


def start_goal(points):
    start = next(p for p, v in points.items() if v == "S")
    end = next(p for p, v in points.items() if v == "E")
    points[start] = "a"
    points[end] = "z"
    return start, end


def path_to(graph, start, end):
    return DijkstraSPF(graph, start).get_path(end)


def solver(lines):
    graph = Graph()
    points = {(x, y): ch for y, line in enumerate(lines) for x, ch in enumerate(line)}
    start, end = start_goal(points)
    y = max(y for _, y in points)
    x = max(x for x, _ in points)
    for p, h in points.items():
        for n in neighbors(p, x, y):
            if distance(p, n, points):
                graph.add_edge(p, n, 1)

    from_S = len(path_to(graph, start, end))

    from_any_a = float("inf")
    for start in tqdm({p for p, v in points.items() if v == "a"}):
        try:
            path = path_to(graph, start, end)
        except KeyError:
            continue
        if path and len(path) < from_any_a:
            from_any_a = len(path)

    return from_S - 1, from_any_a - 1


print("Puzzle Example")
res1, res2 = solver(example(EX_TEXT))
assert (res1, res2) == (31, 29)
print("Puzzle Input")
res1, res2 = solver(puzzle_input())
print(f"Result 1: {res1}")
print(f"Result 2: {res2}")
