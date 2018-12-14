import logging
from blist import blist

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)-15s: %(message)s', level=logging.INFO)


class Score:
    @classmethod
    def make(cls):
        return cls([3, 7], [0, 1])

    def __init__(self, score, elves):
        self.score = blist(score)
        self.elves = elves

    def next(self):
        idx1, idx2 = self.elves
        cur1, cur2 = self.score[idx1], self.score[idx2]
        s = cur1 + cur2
        n1, n2 = (s // 10), s % 10
        score = self.score + blist([n1, n2] if n1 else [n2])
        score_len = len(score)
        elves = [(idx1 + cur1 + 1) % score_len, (idx2 + cur2 + 1) % score_len]
        return Score(score, elves)

    def extend(self, rounds):
        rounds = int(rounds)
        final = self
        while len(final.score) < (rounds + 10):
            final = next(final)
        return final

    def rep(self, start, size):
        start, size = int(start), int(size)
        rep = self.score[start:start+size]
        return ''.join(map(str, rep))

    def search(self, m, idx=0):
        def find_from_here(score_set, idx):
            score_len = len(score_set.score)
            while (idx + size) < score_len:
                rep = score_set.score[idx:idx+size]
                if m == rep:
                    return True, idx
                idx += 1
            return False, idx

        found = False
        score_set = self
        m = map(int, list(str(m)))
        size = len(m)
        while not found:
            found, idx = find_from_here(score_set, idx)
            if not found:
                for _ in range(10000):
                    score_set = next(score_set)
        return idx


def main():
    logger.info("Start")
    with open('input14.txt') as in_file:
        m = in_file.read().strip()

    chocolate = Score.make().extend(2040)
    assert chocolate.rep(9, 10) == '5158916779'
    assert chocolate.rep(5, 10) == '0124515891'
    assert chocolate.rep(18, 10) == '9251071085'
    assert chocolate.rep(2018, 10) == '5941429882'

    chocolate = chocolate.extend(m)
    sol1 = chocolate.rep(m, 10)
    logger.info('Solution #1: %s', sol1)

    assert chocolate.search(51589) == 9
    assert chocolate.search('01245') == 5
    assert chocolate.search(92510) == 18
    assert chocolate.search(59414) == 2018
    chocolate = chocolate.extend(148000000)
    sol2 = chocolate.search(m)
    logger.info('Solution #2: %s', sol2)


main()
