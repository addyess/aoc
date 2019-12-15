from aoc2019.computer import Machine
from PIL import Image, ImageColor

with open("day13.txt") as fin:
    ins = fin.read()


class Video:
    def __init__(self):
        self.outpos = 0
        self.coord = {}
        self.x, self.y = 0, 0
        self.score = 0
        self.prior_ball = None

    def __iter__(self):
        return self

    def find_shape(self, shape):
        for (x, y), z in self.coord.items():
            if z == shape:
                return x, y
        return None

    def __next__(self):
        ball_x, ball_y = self.find_shape(4)
        pad_x, pad_y = self.find_shape(3)

        ball_dir = 0
        if self.prior_ball and (pad_y - ball_y > 1):
            ball_dir = ball_x - self.prior_ball
        self.prior_ball = ball_x
        stick_dir = (ball_x + ball_dir) - pad_x
        return stick_dir/abs(stick_dir) if stick_dir else 0

    def send(self, val):
        self.outpos += 1
        if self.outpos == 1:
            self.x = val
        elif self.outpos == 2:
            self.y = val
        else:
            if (self.x, self.y) == (-1, 0):
                self.score = val
            else:
                self.coord[(self.x, self.y)] = val
            self.outpos = 0

    @property
    def size(self):
        max_x, max_y = -float('inf'), -float('inf')
        for key in self.coord.keys():
            x, y = key
            max_x, max_y = max(x, max_x), max(y, max_y)
        return max_x, max_y

    def render(self):
        max_x, max_y = self.size
        im = Image.new('RGB', (max_x + 1, max_y + 1))
        for x in range(max_x + 1):
            for y in range(max_y + 1):
                pixel = self.coord[(x, y)]
                color = {
                    0: "black",
                    1: "white",
                    2: "green",  #
                    3: "red",    # paddle
                    4: "blue"    # ball
                }.get(pixel)
                im.putpixel((x, y), ImageColor.getcolor(color, 'RGB'))
        im.show()


video = Video()
machine = Machine.decode(ins, video, video)
machine.run()
print(f"Result 1: {len([_ for _ in video.coord.values() if _ == 2])}")

video = Video()
machine = Machine.decode(ins, video, video)
machine.locs[0] = 2
machine.run()
print(f"Result 2: {video.score}")
