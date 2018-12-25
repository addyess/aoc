import re
import logging
from collections import namedtuple
from multiprocessing.dummy import Pool
from z3 import *

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)-15s: %(message)s', level=logging.INFO)
Loc = namedtuple('Loc', 'x,y,z,r')
parse = re.compile(r'pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)')
POOL = Pool()


def make(txt):
    return Loc(*map(int, parse.match(txt.strip()).groups()))


def distance(one, other):
    x1, y1, z1 = one[:-1]
    x2, y2, z2 = other[:-1]
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)


def in_range(one, other):
    return one.r >= distance(one, other)


def z3_abs(x):
    return If(x >= 0, x, -x)


def z3_distance(one, other):
    x1, y1, z1 = one
    x2, y2, z2 = other
    return z3_abs(x1 - x2) + z3_abs(y1 - y2) + z3_abs(z1 - z2)


def finder(bots):
    x = Int('x')
    y = Int('y')
    z = Int('z')
    orig = (x, y, z)
    cost_expr = x * 0

    for bot in bots:
        cost_expr += If(z3_distance(orig, (bot.x, bot.y, bot.z)) <= bot.r, 1, 0)
    opt = Optimize()
    opt.maximize(cost_expr)
    opt.minimize(z3_distance((0, 0, 0), (x, y, z)))
    opt.check()
    model = opt.model()
    best = model[x].as_long(), model[y].as_long(), model[z].as_long()
    return distance(Loc(0, 0, 0, 0), Loc(best[0], best[1], best[2], 0))


def test():
    txt = """pos=<0,0,0>, r=4
            pos=<1,0,0>, r=1
            pos=<4,0,0>, r=3
            pos=<0,2,0>, r=1
            pos=<0,5,0>, r=3
            pos=<0,0,3>, r=1
            pos=<1,1,1>, r=1
            pos=<1,1,2>, r=1
            pos=<1,3,1>, r=1""".split('\n')
    bots = [make(bot) for bot in txt]
    big = sorted(bots, key=lambda b: b.r, reverse=True)
    in_range_of_big = reduce(lambda accum, item: accum + in_range(big[0], item), bots, 0)
    assert 7 == in_range_of_big

    txt = """pos=<10,12,12>, r=2
             pos=<12,14,12>, r=2
             pos=<16,12,12>, r=4
             pos=<14,14,14>, r=6
             pos=<50,50,50>, r=200
             pos=<10,10,10>, r=5""".split('\n')
    bots = [make(bot) for bot in txt]
    best = finder(bots)
    assert best == 36


if __name__ == '__main__':
    test()
    logger.info("Start")
    with open('input23.txt') as in_file:
        bots = []
        for bot in in_file.readlines():
            bot = make(bot)
            bots.append(bot)

    big = sorted(bots, key=lambda b: b.r, reverse=True)
    in_range_of_big = reduce(lambda accum, item: accum + in_range(big[0], item), bots, 0)
    logger.info("Solution #1: %d", in_range_of_big)

    best = finder(bots)
    logger.info("Solution #2: %d", best)
