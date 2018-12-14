import logging
from blist import blist

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)-15s: %(message)s', level=logging.INFO)


class Score:
    @classmethod
    def make(cls):
        return cls([3, 7], (0, 1))

    def __init__(self, score, elves):
        self.score = blist(score)
        self.score_len = len(score)
        self.elves = elves

    def extend(self, rounds):
        elves = self.elves
        while self.score_len < int(rounds):
            cur = self.score[elves[0]], self.score[elves[1]]
            s = sum(cur)
            n1, n2 = (s // 10), s % 10
            self.score.extend([n1, n2] if n1 else [n2])
            self.score_len += 2 if n1 else 1
            elves = (elves[0] + cur[0] + 1) % self.score_len, \
                    (elves[1] + cur[1] + 1) % self.score_len
        self.elves = elves
        return self

    def next_ten(self, start):
        start = int(start)
        if self.score_len < (start+10):
            self.extend(start+10)
        return ''.join(map(str, self.score[start:start+10]))

    def _find_here(self, m, idx):
        size = len(m)
        while (idx + size) < self.score_len:
            rep = self.score[idx:idx + size]
            if m == rep:
                return True, idx
            idx += 1
        return False, idx

    def index_of(self, m, idx=0):
        m = map(int, list(str(m)))
        while True:
            found, idx = self._find_here(m, idx)
            if found:
                return idx
            self.extend(self.score_len + 10000)


def main():
    logger.info("Start")

    chocolate = Score.make()
    assert '5158916779' == chocolate.next_ten(9)
    assert '0124515891' == chocolate.next_ten(5)
    assert '9251071085' == chocolate.next_ten(18)
    assert '5941429882' == chocolate.next_ten(2018)

    with open('input14.txt') as in_file:
        m = in_file.read().strip()
    sol1 = chocolate.next_ten(m)
    logger.info('Solution #1: %s', sol1)

    assert 9 == chocolate.index_of('51589')
    assert 5 == chocolate.index_of('01245')
    assert 18 == chocolate.index_of('92510')
    assert 2018 == chocolate.index_of('59414')
    sol2 = chocolate.index_of(m)
    logger.info('Solution #2: %s', sol2)


main()
