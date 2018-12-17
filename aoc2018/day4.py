import re
import logging
import datetime
logger = logging.getLogger(__name__)

FORMAT = '%(asctime)-15s: %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)


class Log:
    log_re = re.compile(r'\[(.+)\] (.+)').search
    guard_re = re.compile(r'Guard #(\d+) begins shift').search
    datefmt = '%Y-%m-%d %H:%M'

    def __init__(self, txt):
        self.txt = txt.strip()
        ts, event = self.log_re(self.txt).groups()
        self._time = datetime.datetime.strptime(ts, self.datefmt)
        self.event = event

    def time(self):
        return self._time

    @property
    def guard_id(self):
        m = self.guard_re(self.event)
        if m:
            guard_id, = m.groups()
            return int(guard_id)
        return None

    @property
    def wakes(self):
        return 'wakes' in self.event

    @property
    def sleeps(self):
        return 'asleep' in self.event


class Guard:
    def __init__(self, _id):
        self.id = _id
        self._total = 0
        self._last_event = None
        self.sleeps = []

    def add(self, event):
        if event.wakes:
            last = self._last_event
            duration = event.time() - last.time()
            self._total += duration.total_seconds()
            self.sleeps += [(last.time(), event.time())]
        self._last_event = event

    def total(self):
        return self._total // 60

    def frequency(self):
        d = {k: 0 for k in range(0, 60)}
        longest = (0, 0)
        for start, end in self.sleeps:
            for i in range(start.minute, end.minute):
                d[i] += 1
                if max(d[i], longest[0]) == d[i]:
                    longest = (d[i], i)
        return longest

    def __repr__(self):
        return 'Guard({})'.format(self.id)


def main():
    logger.info("Start")
    with open('input4.txt') as f:
        logs = sorted([Log(i) for i in f.readlines() if i], key=Log.time)

    def get_guard(gid):
        sched[gid] = guard = sched.get(gid) or Guard(gid)
        return guard

    def handle_event(e, current):
        if e.guard_id or current is None:
            current = get_guard(e.guard_id)
        else:
            current.add(e)
        return current

    g = None
    sched = {}
    for log in logs:
        g = handle_event(log, g)

    most_asleep = sorted(sched.values(), key=Guard.total)
    sleepiest = most_asleep[-1]
    logger.info("Solution #1 %s sleeps: %s min", sleepiest, sleepiest.total())
    logger.info("Solution #1 %s overlaps %s", sleepiest, sleepiest.frequency())
    logger.info("Solution #1 Product Output: %d", sleepiest.id * sleepiest.frequency()[1])

    most_freq = sorted(sched.values(), key=Guard.frequency)
    sleepiest = most_freq[-1]
    logger.info("Solution #2 %s overlaps %s", sleepiest, sleepiest.frequency())
    logger.info("Solution #2 Product Output: %d", sleepiest.id * sleepiest.frequency()[1])


if __name__ == '__main__':
    main()
