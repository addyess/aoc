import logging
from itertools import count
from collections import namedtuple

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)-15s: %(message)s', level=logging.INFO)
Pot = namedtuple('Pot', ['idx', 'state'])


def note(txt):
    llcrr, _ = txt.split(' => ')
    return [c == '#' for c in llcrr]


class Pots:
    @classmethod
    def create(cls, initial, notes):
        state = [Pot(idx, char == '#') for idx, char in enumerate(initial)]
        notes = [note(arg) for arg in notes if arg.endswith('#')]
        return cls(state, notes)

    def __init__(self, state, notes):
        self.state = state
        self.notes = notes
        self._sum = None

    def next(self):
        result = []
        it = self.state
        front, end = it[0], it[-1]
        it = [Pot(front.idx - x, False) for x in range(4, 0, -1)] + \
            it + [Pot(end.idx + x, False) for x in range(1, 5)]

        last = 0
        for idx, elem in enumerate(it):
            nodes = [p.state for p in it[idx-2:idx+3]]
            match = nodes and any(n == nodes for n in self.notes)
            if match or result:  # Ignore all empty pots until first full pot
                result.append(Pot(elem.idx, match))
                last = len(result) if match else last
        return Pots(result[:last], self.notes)  # Drop all ending empty pots

    def sum(self, adder=0):
        self._sum = self._sum or sum([pot.idx + adder for pot in self.state if pot.state])
        return self._sum

    def stable(self, generational_sum):
        last_sum, pots, c = 0, self, count()
        for idx in c:
            new_sum = pots.sum(generational_sum - idx)
            if last_sum == new_sum:
                break
            last_sum, pots = new_sum, next(pots)
        return last_sum

    def generate(self, gens):
        pots = self
        for _ in xrange(0, gens):
            pots = next(pots)
        return pots


def main():
    logger.info("Start")
    with open('input12.txt') as in_file:
        initial = next(in_file).strip('initial state: ').strip()
        notes = filter(None, (_.strip() for _ in in_file if _))
        p = Pots.create(initial, notes)

    sol1 = p.generate(20).sum()
    logger.info('Solution #1: %s', sol1)
    logger.info('Solution #2: %s', p.stable(50000000000))

main()
