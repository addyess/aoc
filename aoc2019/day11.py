from collections import defaultdict
from aoc2019.computer import Machine
from PIL import Image, ImageColor

with open("day11.txt") as fin:
    ins = fin.read()


class License:
    UP = 0, -1
    DN = 0, 1
    LT = -1, 0
    RT = 1, 0

    def __init__(self, starter):
        self.outpos = True
        self.pos = 0, 0
        self.dir = self.UP
        self.coordinates = defaultdict(int, {self.pos: starter})

    def turn(self, val):
        new_dir = self.RT if val else self.LT
        if self.dir == self.DN:
            new_dir = self.LT if val else self.RT
        elif self.dir == self.RT:
            new_dir = self.DN if val else self.UP
        elif self.dir == self.LT:
            new_dir = self.UP if val else self.DN
        self.pos = tuple(sum(x) for x in zip(self.pos, new_dir))
        self.dir = new_dir

    def __iter__(self):
        return self

    def __next__(self):
        return self.coordinates[self.pos]  # return current color

    def send(self, val):
        if self.outpos:
            self.coordinates[self.pos] = val
        else:
            self.turn(val)
        self.outpos = not self.outpos

    @property
    def size(self):
        max_x, max_y = -float('inf'), -float('inf')
        for key in self.coordinates.keys():
            x, y = key
            max_x, max_y = max(x, max_x), max(y, max_y)
        return max_x, max_y

    def render(self):
        max_x, max_y = self.size
        im = Image.new('1', (max_x + 1, max_y + 1))
        for x in range(max_x + 1):
            for y in range(max_y + 1):
                pixel = self.coordinates[(x, y)]
                color = 'black' if pixel == 0 else 'white'
                im.putpixel((x, y), ImageColor.getcolor(color, '1'))
        im.show()


lic = License(0)
machine = Machine.decode(ins, lic, lic)
machine.run()
print(f"Result 1: {len(lic.coordinates)}")

lic = License(1)
machine = Machine.decode(ins, lic, lic)
machine.run()
lic.render()
