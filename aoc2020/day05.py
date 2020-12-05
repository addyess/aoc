from itertools import dropwhile
with open("day05.txt") as f_in:
    ins = [_.strip() for _ in f_in]


def parsed(stream):
    """Create a list of numbers created from binary definition of seats."""
    s_map = str.maketrans({'F': '0', 'B': '1', 'R': '1', 'L': '0'})
    return sorted([int(s.translate(s_map), 2) for s in stream])


def missing(_seats):
    """Find the first seat that doesn't match it's index + seats[0]."""
    it = dropwhile(lambda x: x[0] == x[1], enumerate(_seats, _seats[0]))
    return next(it)[0]  # first seat that isn't filled


seats = parsed(ins)
print(f"Result 1: {max(seats)}")
print(f"Result 2: {missing(seats)}")
