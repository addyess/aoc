import logging
from itertools import imap, islice

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)-15s: %(message)s', level=logging.INFO)
logger.info("Start")


class Nodes:
    @classmethod
    def from_file(cls, f):
        return cls(f.read().strip().split(' '))

    def __init__(self, seq):
        self.seq = seq

    def sol1(self):
        def recurse(seq):
            num, meta = next(seq), next(seq)
            return sum(recurse(seq) for _ in range(0, num)) + sum(islice(seq, meta))
        return recurse(imap(int, self.seq))

    def sol2(self):
        def recurse(seq):
            num, meta = next(seq), next(seq)
            child_sums = [recurse(seq) for _ in range(0, num)]
            meta_data = islice(seq, meta)
            return sum(
                meta_data if num == 0 else
                (child_sums[idx - 1] for idx in meta_data if (idx - 1) < len(child_sums))
            )
        return recurse(imap(int, self.seq))

    def solve(self):
        return self.sol1(), self.sol2()


def main():
    with open('input8.txt') as f:
        n = Nodes.from_file(f)

    sol1, sol2 = n.solve()
    logger.info('Solution #1 -- %s' % sol1)
    logger.info('Solution #2 -- %s' % sol2)


main()
