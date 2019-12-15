import re
from itertools import count
from concurrent.futures import ThreadPoolExecutor

with open("day12.txt") as fin:
    ins = fin.read()


class Moon:
    init_re = re.compile(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>")

    @classmethod
    def from_line(cls, line):
        return cls(tuple(int(_) for _ in cls.init_re.search(line).groups()))

    def __init__(self, pos, vel=(0, 0, 0), acc=(0, 0, 0)):
        self.pos = pos
        self.vel = vel

    def gravity(self, system):
        updates = [
            [
                0 if me == it else (1 if me < it else -1)
                for me, it in zip(self.pos, moon.pos)
            ]
            for moon in system.moons
            if moon != self
        ]
        new_vel = tuple(sum(vecs) for vecs in zip(self.vel, *updates))
        return new_vel

    def move(self, new_vel):
        new_pos = tuple(sum(it) for it in zip(self.pos, new_vel))
        return Moon(new_pos, new_vel)

    def __eq__(self, other):
        return self.pos == other.pos and self.vel == other.vel

    def __ne__(self, other):
        return not (self == other)

    @property
    def potential(self):
        return sum(map(abs, self.pos))

    @property
    def kenetic(self):
        return sum(map(abs, self.vel))

    @property
    def total_energy(self):
        return self.kenetic * self.potential

    def __repr__(self):
        return f'Moon({self.pos}, {self.vel})'


class System:
    @classmethod
    def from_text(cls, text):
        return cls([
            Moon.from_line(line)
            for line in text.strip().splitlines()
        ])

    def __init__(self, moons):
        self.first_moons = moons.copy()
        self.moons = moons

    def step(self):
        new_vel = [_.gravity(self) for _ in self.moons]
        new_moons = [_.move(v) for _, v in zip(self.moons, new_vel)]
        old_moons, self.moons = self.moons, new_moons

    def run(self, total):
        self.moons = self.first_moons
        for idx in range(total):
            self.step()
        return self.total_energy

    @property
    def total_energy(self):
        return sum(_.total_energy for _ in self.moons)

    def steps_to_repeat_pos(self, dim):
        self.moons = self.first_moons
        dims = [(_.pos[dim],_.vel[dim]) for _ in self.first_moons]
        period = lambda m: [(_.pos[dim], _.vel[dim]) for _ in m]
        for idx in count():
            self.step()
            if period(self.moons) == dims:
                idx += 1
                break
        return idx

    def steps_to_repeat(self):
        a, b, c = (self.steps_to_repeat_pos(_) for _ in range(3))
        return lcm(lcm(a, b), c)


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    return (a // gcd(a, b)) * b


sys = System.from_text(ins)
print(f"Result 1: {sys.run(1000)}")
print(f"Result 2: {sys.steps_to_repeat()}")
