from collections import namedtuple
from functools import partial
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)-15s: %(message)s', level=logging.INFO)
Point = namedtuple('Point', 'x,y,z,t')


def distance(p1, p2):
    return sum(map(lambda (x, z): abs(x - z), zip(p1, p2)))


def add_point(p1, consts):
    for const in consts:
        for p2 in const:
            if distance(p1, p2) <= 3:
                const.add(p1)
                return None
    consts.append({p1})


def merge(consts):
    for idx, const in enumerate(consts):
        for other_const in consts[idx + 1:]:
            if any(distance(p1, p2) <= 3 for p1 in const for p2 in other_const):
                const.update(other_const)  # update constellation
                other_const.clear()        # empty merged set
    return filter(None, consts)


def count_constellations(points):
    consts = []
    for point in points:
        add_point(point, consts)

    pre_len, tot_len = 0, len(consts)
    while pre_len != tot_len:
        pre_len = tot_len
        consts = merge(consts)
        tot_len = len(consts)

    return tot_len


def main():
    logger.info("Start")
    with open('input25.txt') as in_file:
        points = [Point(*eval('(' + line.strip() + ')')) for line in in_file if line.strip()]
    sol1 = count_constellations(points)
    assert sol1 == 367
    logger.info("Solution #1: %d", sol1)


if __name__ == '__main__':
    main()


def test():
    txt = """
     0,0,0,0
     3,0,0,0
     0,3,0,0
     0,0,3,0
     0,0,0,3
     0,0,0,6
     9,0,0,0
    12,0,0,0    
    """.split('\n')
    points = [Point(*eval('(' + line.strip() + ')')) for line in txt if line.strip()]
    assert count_constellations(points) == 2

    txt = """
    -1,2,2,0
    0,0,2,-2
    0,0,0,-2
    -1,2,0,0
    -2,-2,-2,2
    3,0,2,-1
    -1,3,2,2
    -1,0,-1,0
    0,2,1,-2
    3,0,0,0""".split('\n')
    points = [Point(*eval('(' + line.strip() + ')')) for line in txt if line.strip()]
    assert count_constellations(points) == 4

    txt = """
    1,-1,0,1
    2,0,-1,0
    3,2,-1,0
    0,0,3,1
    0,0,-1,-1
    2,3,-2,0
    -2,2,0,0
    2,-2,0,-1
    1,-1,0,-1
    3,2,0,2""".split('\n')
    points = [Point(*eval('(' + line.strip() + ')')) for line in txt if line.strip()]
    assert count_constellations(points) == 3

    txt = """
    1,-1,-1,-2
    -2,-2,0,1
    0,2,1,3
    -2,3,-2,1
    0,2,3,-2
    -1,-1,1,-2
    0,-2,-1,0
    -2,2,3,-1
    1,2,2,0
    -1,-2,0,-2""".split('\n')
    points = [Point(*eval('(' + line.strip() + ')')) for line in txt if line.strip()]
    assert count_constellations(points) == 8
