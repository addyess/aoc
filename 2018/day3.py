import logging
import re
logger = logging.getLogger(__name__)


class Claim:
    txt_re = re.compile(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")

    def __init__(self, **kwargs):
        txt = kwargs.get('txt')
        if txt:
            m = self.txt_re.search(txt)
            (
                self.id,
                x, y, w, h
            ) = m.groups()
        else:
            x, y, w, h = [
                kwargs.get(l) for l in ['xywh']
            ]
        self.x = int(x)
        self.y = int(y)
        self.w = int(w)
        self.h = int(h)
        self._collides = False

    def __repr__(self):
        return """Claim(id='{}',x={}, y={},w={}, h={})""".format(
            self.id, self.x, self.y, self.w, self.h
        ).replace('\n', '')

    def collide(self):
        if not self._collides:
            self._collides = True

    @property
    def isolated(self):
        return not self._collides


DEM = 1000


class Master:
    def __init__(self):
        self.map = [[[] for _ in range(0, DEM)] for _ in range(0, DEM)]
        self.overlaps = 0

    def place(self, c):
        for x in range(0, c.w):
            for y in range(0, c.h):
                self.map[c.x + x][c.y + y].append(c)
                cur = self.map[c.x + x][c.y + y]
                if len(cur) == 2:      # 2nd claim on same spot
                    self.overlaps += 1
                if len(cur) > 1:       # Not first claim on spot
                    for mark in cur:
                        mark.collide()
        return c


def main():
    m = Master()
    with open('input3.txt') as f:
        claims = [m.place(Claim(txt=i)) for i in f.readlines() if i]

    logger.info("Solution #1: (%d)", m.overlaps)
    for claim in claims:
        if claim.isolated:
            logger.info("Solution #2: (%s):", claim.id)


if __name__ == '__main__':
    FORMAT = '%(asctime)-15s: %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO)
    logger.info("Start")
    main()
