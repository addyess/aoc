import logging
import re
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)-15s: %(message)s', level=logging.INFO)
logger.info("Start")

parse_re = re.compile(r'Step (\S) must be finished before step (\S) can begin.')


class Graph:
    @classmethod
    def from_list(cls, f):
        c = cls()
        [c.insert(*parse_re.search(l).groups()) for l in f]
        return c

    def __init__(self):
        self.d = {}

    def insert(self, _from, _to):
        if _from in self.d:
            self.d[_from].update(_to)
        else:
            self.d[_from] = {_to}
        if _to not in self.d:
            self.d[_to] = set()

    @staticmethod
    def front(d):
        return {
            k for k in d.keys()
            if not any(True for v in d.values() if k in v)
        }

    def order(self):
        def run(d):
            if len(d) == 1:
                return d.keys()[0]
            head = sorted(self.front(d))[0]
            d.pop(head)
            return head + run(d)
        return run(self.d.copy())

    def schedule(self):
        def next_job():
            working = {e.work.name for e in elves if e.work}
            available = self.front(d).difference(working)
            return sorted(available)[0] if available else None

        def assign(e):
            n = next_job()
            e.work = Work(n) if n else None

        def tick(e):
            d.pop(e.tick(), None)

        ticks = 0
        elves = [Worker() for _ in range(0, WORKERS)]
        d = self.d.copy()
        while d:
            ticks += 1
            [assign(elf) for elf in elves if elf.work is None]
            [tick(elf) for elf in elves]
        return ticks


class Work:
    def tick(self):
        self.remaining -= 1
        return self.remaining == 0

    def __init__(self, v):
        self.name = v
        self.remaining = DURATION + ord(self.name) - 64


class Worker(object):
    work = None

    def tick(self):
        if self.work and self.work.tick():
            w = self.work
            self.work = None
            return w.name
        return None


DURATION = 60
WORKERS = 5


def main():
    with open('input7.txt') as f:
        g = Graph.from_list(f)

    sol1, sol2 = g.order(), g.schedule()
    assert sol1 == 'BFKEGNOVATIHXYZRMCJDLSUPWQ'
    assert sol2 == 1020
    logger.info('Solution #1 -- %s' % sol1)
    logger.info('Solution #2 -- %s' % sol2)


main()
