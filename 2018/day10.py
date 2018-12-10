import logging
from itertools import imap
import re

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)-15s: %(message)s', level=logging.INFO)
logger.info("Start")
parser = re.compile(r'position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>')


class StarMap:
    def __init__(self, f):
        self.found = None
        self.seconds = 0
        self.stars = [
            tuple(imap(int, parser.search(txt).groups()))
            for txt in f
        ]

    def smallest(self, img):
        img_area = (img.height * img.width) if img else 0
        f_area = (self.found.height * self.found.width) if self.found else ''
        if img:
            if img_area < f_area:
                self.found = img
            elif img_area > f_area:
                return self.found
        return None

    def draw_tick(self, step):
        from PIL import Image, ImageDraw
        minx = min(imap(lambda _: _[0], step))
        miny = min(imap(lambda _: _[1], step))
        maxx = max(imap(lambda _: _[0], step))
        maxy = max(imap(lambda _: _[1], step))
        xsize = maxx - minx
        ysize = maxy - miny
        img, draw = None, None
        minimum_draw_size = len(step) / 4

        if xsize < minimum_draw_size or ysize < minimum_draw_size:
            img = Image.new("RGB", (xsize + 5, ysize + 5), "white")
            img.seconds = self.seconds
            draw = ImageDraw.Draw(img)

        def add_pixel(args):
            x, y, vx, vy = args
            if draw:
                draw.rectangle([
                    (x - minx, y - miny),
                    (x - minx + DOT_SIZE - 1, y - miny + DOT_SIZE - 1)
                ], fill='black')
            return x+vx, y+vy, vx, vy

        step = map(add_pixel, step)
        self.seconds += 1
        return step, img

    def locate(self):
        step = self.stars
        while True:
            step, drawn = self.draw_tick(step)
            smallest = self.smallest(drawn)
            if smallest:
                smallest.show()
                return smallest.seconds

DOT_SIZE = 1


with open('input10.txt') as in_file:
    m = StarMap(in_file)
logger.info('Solution #2: %d (sec)', m.locate())
