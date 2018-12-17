import logging

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)-15s: %(message)s', level=logging.INFO)


class Score:
    @classmethod
    def make(cls):
        return cls([3, 7], (0, 1))

    def __init__(self, score, elves):
        self.score = list(score)
        self.elves = elves

    def _extend(self, rounds):
        elves = self.elves
        while len(self.score) < int(rounds):
            cur = self.score[elves[0]], self.score[elves[1]]
            s = sum(cur)
            n1, n2 = (s // 10), s % 10
            self.score.extend([n1, n2] if n1 else [n2])
            elves = (elves[0] + cur[0] + 1) % len(self.score), \
                    (elves[1] + cur[1] + 1) % len(self.score)
        self.elves = elves
        return self

    def next_ten(self, start):
        start = int(start)
        if len(self.score) < (start+10):
            self._extend(start+10)
        return ''.join(map(str, self.score[start:start+10]))

    def _find_here(self, m, idx):
        size = len(m)
        while (idx + size) < len(self.score):
            rep = self.score[idx:idx + size]
            if m == rep:
                return True, idx
            idx += 1
        return False, idx

    def index(self, m, idx=0):
        m = list(map(int, str(m)))
        while True:
            found, idx = self._find_here(m, idx)
            if found:
                return idx
            self._extend(len(self.score) + 10000)


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

    assert 9 == chocolate.index('51589')
    assert 5 == chocolate.index('01245')
    assert 18 == chocolate.index('92510')
    assert 2018 == chocolate.index('59414')
    sol2 = chocolate.index(m)
    logger.info('Solution #2: %s', sol2)


main()
