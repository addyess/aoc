from functools import cached_property


class Algorithm:
    @classmethod
    def parse(cls, line):
        return cls(line.strip())

    def __init__(self, data):
        self.data = data

    def __getitem__(self, item: str):
        idx = sum((2 ** bit) * (v == "#") for bit, v in enumerate(reversed(item)))
        return self.data[idx] == "#"


class Boundary:
    def __init__(self, x, y):
        self.mx, self.Mx = min(x), max(x)
        self.my, self.My = min(y), max(y)

    def __contains__(self, item):
        x, y = item
        return (self.mx <= x <= self.Mx) and (self.my <= y <= self.My)


class Image:
    @classmethod
    def parse(cls, lines):
        return cls(
            {
                (x, y)
                for y, line in enumerate(lines)
                for x, p in enumerate(line.strip())
                if p == "#"
            },
            ".",
        )

    def __init__(self, pixels, border):
        self.pixels = pixels
        self.border = border

    @cached_property
    def boundary(self):
        return Boundary(*zip(*self.pixels))

    def cell(self, x, y):
        return "".join(
            "#"
            if (xr, yr) in self.pixels
            else ("." if (xr, yr) in self.boundary else self.border)
            for yr in range(y - 1, y + 2)
            for xr in range(x - 1, x + 2)
        )

    def generate(self, algorithm):
        bx, by = self.boundary.mx - 3, self.boundary.my - 3
        border = "#" if algorithm[self.cell(bx, by)] else "."
        gen = (
            (x, y, algorithm[self.cell(x, y)])
            for x in range(self.boundary.mx - 2, self.boundary.Mx + 3)
            for y in range(self.boundary.my - 2, self.boundary.My + 3)
        )
        return Image({(x, y) for x, y, v in gen if v}, border)


with open("day20.txt") as fin:
    iea = Algorithm.parse(next(fin))
    next(fin)  # skip blank line
    image = Image.parse(fin)

for it in range(50):
    image = image.generate(iea)
    if it == 1:
        print(f"Result 1 {len(image.pixels)}")
print(f"Result 2 {len(image.pixels)}")
