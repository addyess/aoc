from itertools import count

class CucumberMap:
    @classmethod
    def parse(cls, lines):
        return cls({
            (x, y): faces
            for y, line in enumerate(lines)
            for x, faces in enumerate(line.strip())
        }, )

    def __eq__(self, other):
        return self.coords == other.coords

    def __str__(self):
        return "\n".join(
            "".join(self.coords.get((x, y), '.') for x in range(self.boundary[0]))
            for y in range(self.boundary[1])
        ) + "\n"

    def __init__(self, coords, bounds=None):
        if not bounds:
            x, y = zip(*coords.keys())
            self.boundary = max(x) + 1, max(y) + 1
        else:
            self.boundary = bounds
        self.coords = {it: faces for it, faces in coords.items() if faces != "."}

    @staticmethod
    def next_move(mapped, boundary, coord, faces):
        if faces == '>':
            step = ((coord[0] + 1) % boundary[0], coord[1])
        else:
            step = (coord[0], (coord[1]+1) % boundary[1])
        if not mapped.get(step):
            return step, faces
        return coord, faces

    def single_step(self):
        east = {
            coord: self.next_move(self.coords, self.boundary, coord, faces)
            for coord, faces in self.coords.items()
            if faces == '>'
        }
        mapped = dict(self.coords)
        for c_from, (c_to, faces) in east.items():
            mapped.pop(c_from)
            mapped[c_to] = faces
        south = dict(
            self.next_move(mapped, self.boundary, coord, faces)
            for coord, faces in self.coords.items()
            if faces == 'v'
        )
        new_coord = {**dict(east.values()), **south}
        return CucumberMap(new_coord, self.boundary)


def main(fname):
    with open(fname) as fin:
        seafloor = CucumberMap.parse(fin)
    for c in count():
        seafloor, last = seafloor.single_step(), seafloor
        if seafloor == last:
            return c+1

print(f'Result #1: {main("day25.txt")}')