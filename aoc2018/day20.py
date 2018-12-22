import logging
from collections import namedtuple
from astar import AStar
from math import hypot

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)-15s: %(message)s', level=logging.INFO)
Loc = namedtuple('Loc', 'x, y')


class Room(Loc):
    def __init__(self, *args):
        super(Room, self).__init__(*args)
        self.neighbors = set()

    @property
    def loc(self):
        return tuple(self)


E = lambda l: Room(l.x + 1, l.y)
W = lambda l: Room(l.x - 1, l.y)
N = lambda l: Room(l.x, l.y + 1)
S = lambda l: Room(l.x, l.y - 1)


class HQMap(AStar):
    def __init__(self, rooms):
        self.start = Room(0, 0)
        self.rooms = rooms
        self._most_doors = None
        self._rooms_over = {}
        self._paths = None

    @classmethod
    def from_regex(cls, pattern):
        hq = cls(set())
        stack, room = [], hq.start
        for p in pattern:
            if p == '^':
                continue
            elif p == '$':
                break
            elif p == '(':
                stack.append(room)
            elif p == '|':
                room = stack[-1]
            elif p == ')':
                stack.pop()
            elif p in 'WNSE':
                new_room = eval(p)(room)
                room.neighbors.add(new_room)
                room = new_room
                hq.rooms.add(room)
        return hq

    def neighbors(self, node):
        return node.neighbors

    def distance_between(self, n1, n2):
        return 1

    def heuristic_cost_estimate(self, current, goal):
        (x1, y1) = current.loc
        (x2, y2) = goal.loc
        return hypot(x2 - x1, y2 - y1)

    @property
    def paths(self):
        if self._paths is None:
            astars = map(list, (
                self.astar(self.start, room)
                for room in self.rooms if room != self.start
            ))
            self._paths = sorted(astars, key=len, reverse=True)
        return self._paths

    @property
    def most_doors(self):
        if self._most_doors is None:
            self._most_doors = len(self.paths[0]) - 1
        return self._most_doors

    def doors_over(self, distance):
        doors_over = self._rooms_over.get(distance)
        if doors_over is None:
            doors_over = len([l for l in self.paths if (len(l)) > distance])
            self._rooms_over[distance] = doors_over
        return doors_over


if __name__ == '__main__':
    logger.info("Start")
    hq = HQMap.from_regex('^WNE$')
    assert hq.most_doors == 3
    assert hq.doors_over(2) == 2
    hq = HQMap.from_regex('^ENWWW(NEEE|SSE(EE|N))$')
    assert hq.most_doors == 10
    hq = HQMap.from_regex('^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$')
    assert hq.most_doors == 18
    hq = HQMap.from_regex("^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$")
    assert hq.most_doors == 23
    hq = HQMap.from_regex("^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$")
    assert hq.most_doors == 31

    with open('input20.txt') as in_file:
        hq = HQMap.from_regex(in_file.read().strip())
    logger.info("Solution #1: %d", hq.most_doors)
    logger.info("Solution #2: %d", hq.doors_over(1000))
