import logging
from itertools import takewhile, imap
from collections import namedtuple

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)-15s: %(message)s', level=logging.INFO)
logger.info("Start")
GRID_SZ = 300
Cell = namedtuple('Cell', ['sum', 'x', 'y', 'n'])


class FuelCellGrid:
    def __init__(self, ser):
        self.ser = ser
        self._grid = None

    def power_at(self, x, y):
        rack_id = x + 10
        return ((((rack_id * y) + self.ser) * rack_id) / 100) % 10 - 5

    def power_nxn_at(self, x, y, n):
        return sum([self.grid[y + dy - 1][x + dx - 1] for dx in range(n) for dy in range(n)])

    @property
    def grid(self):
        if self._grid is None:
            self._grid = [[self.power_at(x + 1, y + 1)
                           for x in range(GRID_SZ)]
                          for y in range(GRID_SZ)]
        return self._grid

    def most_power(self, n):
        all_powers = ((self.power_nxn_at(x + 1, y + 1, n), (x + 1, y + 1))
                      for x in range(GRID_SZ - n + 1)
                      for y in range(GRID_SZ - n + 1))
        ans = sorted(all_powers)[-1]
        logger.info('Calculating {n} x {n} is {m}'.format(n=n, m=ans))
        return Cell(ans[0], ans[1][0], ans[1][1], n)


assert FuelCellGrid(8).power_at(3, 5) == 4
assert FuelCellGrid(57).power_at(122, 79) == -5
assert FuelCellGrid(39).power_at(217, 196) == 0
assert FuelCellGrid(71).power_at(101, 153) == 4
assert FuelCellGrid(18).power_nxn_at(33, 45, 3) == 29
assert FuelCellGrid(42).power_nxn_at(21, 61, 3) == 30

with open('input11.txt') as in_file:
    m = FuelCellGrid(int(in_file.read()))

power_levels = list(takewhile(lambda i: i[0] > 0, imap(m.most_power, xrange(1, 300))))
sol1 = power_levels[2]
sol2 = sorted(power_levels)[-1]

logger.info('Solution #1: %s,%s', sol1.x, sol1.y)
logger.info('Solution #2: %s,%s,%s', sol2.x, sol2.y, sol2.n)
