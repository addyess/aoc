import re


class Cuboid:
    step_re = re.compile(
        r"(?P<state>on|off) x=(?P<x1>-?\d+)..(?P<x2>-?\d+),y=(?P<y1>-?\d+)..(?P<y2>-?\d+),z=(?P<z1>-?\d+)..(?P<z2>-?\d+)")

    @classmethod
    def parse(cls, lines):
        gen = (cls.step_re.match(line) for line in lines)
        return [cls(*(m.group(_) for _ in ['state', 'x1', 'x2', 'y1', 'y2', 'z1', 'z2'])) for m in gen if m]

    def __init__(self, state, x1, x2, y1, y2, z1, z2):
        self.state = state == 'on'
        self.x = int(x1), int(x2) + 1
        self.y = int(y1), int(y2) + 1
        self.z = int(z1), int(z2) + 1

    def cubes(self, reduce_region=True):
        if reduce_region:
            for dim in 'xyz':
                new = list(getattr(self, dim))
                if new[0] < -50:
                    new[0] = -50
                if new[1] > 51:
                    new[1] = 51
                if not all(-50 <= _ <= 51 for _ in new):
                    return set()
                setattr(self, dim, tuple(new))
        return {
            (x, y, z)
            for x in range(*self.x)
            for y in range(*self.y)
            for z in range(*self.z)
        }


with open("day22.txt") as fin:
    cuboids = Cuboid.parse(fin)

cubes_on = set()
for cuboid in cuboids:
    if cuboid.state:
        cubes_on |= cuboid.cubes()
    else:
        cubes_on -= cuboid.cubes()

print(f"Result #1: {len(cubes_on)}")
