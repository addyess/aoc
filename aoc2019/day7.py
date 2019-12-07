from itertools import permutations, chain
from aoc2019.computer import Machine
from threading import Event
from concurrent.futures import ThreadPoolExecutor

with open("day7.txt") as fin:
    ins = fin.read()

max_out = -1
for phases in permutations(range(0, 5)):
    out = 0
    for phase in phases:
        amp = Machine.decode(ins, [phase, out])
        out, = amp.run()
    if out > max_out:
        max_out = out

print(f"Result 1: {max_out}")


class Wire:
    def __init__(self):
        self.value = None
        self.e = Event()

    def __iter__(self):
        return self

    def __next__(self):
        self.e.wait()
        self.e.clear()
        return self.value

    def send(self, val):
        self.value = val
        self.e.set()


max_out = -1
for phases in permutations(range(5, 10)):
    amps = []
    prior = [0]
    for phase in phases:
        m = Machine.decode(ins, chain([phase], prior), Wire())
        amps.append(m)
        prior = m.stdout
    amps[0].stdin = chain(amps[0].stdin, amps[-1].stdout)

    with ThreadPoolExecutor(max_workers=len(amps)) as executor:
        executor.map(Machine.run, amps)

    if amps[-1].stdout.value > max_out:
        max_out = amps[-1].stdout.value

print(f"Result 2: {max_out}")
