import logging
from itertools import imap
import re

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)-15s: %(message)s', level=logging.INFO)
logger.info("Start")
parser = re.compile(r'position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>')


class Image:
    def __init__(self, stars, wh, xy, seconds):
        self.stars, self.seconds = stars, seconds
        self.width, self.height = wh
        self.area = self.width * self.height
        self.minx, self.miny = xy

    def show(self):
        disp = [None] * (self.height + 1)
        for h in range(self.height + 1):
            disp[h] = [' '] * (self.width + 1)

        for star in self.stars:
            disp[star[1] - self.miny][star[0] - self.minx] = '#'
        logger.info("Solution #1: \n%s\n", '\n'.join(''.join(row) for row in disp))


class StarMap:
    def __init__(self, f):
        self.found = None
        self.stars = [
            tuple(imap(int, parser.search(txt).groups()))
            for txt in f
        ]

    def smallest(self, img):
        if img:
            f_area = self.found.area if self.found else ''
            if img.area < f_area:
                self.found = img
            elif img.area > f_area:
                return self.found

    def tick(self, stars, seconds):
        minimum_draw_size = len(stars) / 4
        minx, miny, maxx, maxy = '', '', 0, 0
        new_stars = []
        for x, y, vx, vy in stars:
            minx = min(x, minx)
            miny = min(y, miny)
            maxx = max(x, maxx)
            maxy = max(y, maxy)
            new_stars.append((x+vx, y+vy, vx, vy))
        xsize = maxx - minx
        ysize = maxy - miny
        img = None
        seconds += 1
        if xsize < minimum_draw_size or ysize < minimum_draw_size:
            img = Image(stars, (xsize, ysize), (minx, miny), seconds)
        return new_stars, img, seconds

    def locate(self):
        seconds, smallest, stars = 0, None, self.stars
        while not smallest:
            stars, img, seconds = self.tick(stars, seconds)
            smallest = self.smallest(img)
        return smallest


with open('input10.txt') as in_file:
    m = StarMap(in_file)

solution = m.locate()
solution.show()
logger.info('Solution #2: %d (sec)', solution.seconds)

