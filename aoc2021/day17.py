import re

start = 0, 0
target = "target area: x=20..30, y=-10..-5"


class Range:
    @classmethod
    def parse(cls, s_target):
        m = re.match(
            r"target area: x=(?P<x1>-?\d+)..(?P<x2>-?\d+), y=(?P<y1>-?\d+)..(?P<y2>-?\d+)",
            s_target,
        )
        return cls({k: int(v) for k, v in m.groupdict().items()})

    def __init__(self, vectors):
        self.spec = vectors

    def evaluate(self, pos):
        x, y = pos
        if (
            self.spec["x1"] <= x <= self.spec["x2"]
            and self.spec["y1"] <= y <= self.spec["y2"]
        ):
            return 0  # hit
        elif y < self.spec["y1"] or x > self.spec["x2"]:
            return 1  # deep
        return -1

    def steps(self, vel):
        pos = 0, 0
        is_hit = -1
        steps = [pos]
        while is_hit == -1:
            px, py = pos
            vx, vy = vel
            npx = px + vx
            npy = py + vy
            vx = vx and (vx + 1 if vx < 0 else vx - 1)
            vy -= 1
            pos, vel = (npx, npy), (vx, vy)
            steps += [pos]
            is_hit = self.evaluate(pos)
        if is_hit == 0:
            return steps

    def potential_x_target(self):
        for x in range(self.spec["x1"], self.spec["x2"] + 1):
            yield x

    def potential_x_vel(self):
        for pot_x in self.potential_x_target():
            dir_x, val_x = -1 if pot_x < 0 else 1, abs(pot_x)
            for pos_xv in range(val_x + 1):
                for end_xv in range(pos_xv + 1):
                    if sum(range(end_xv, pos_xv + 1)) == pot_x:
                        yield pos_xv * dir_x

    def highest_launch_metrics(self):
        highest = -float("inf")
        x_spec = self.spec["x1"] // 2
        pot_vx = set(self.potential_x_vel())
        for vx in pot_vx:
            for vy in range(x_spec):
                steps = self.steps((vx, vy))
                if steps:
                    highest = max(highest, max(steps, key=lambda p: p[1])[1])
        return highest

    def successful_launch_metrics(self):
        success = []
        x_spec = self.spec["x1"] // 2
        pot_vx = set(self.potential_x_vel())
        for vx in pot_vx:
            for vy in range(-x_spec, x_spec):
                steps = self.steps((vx, vy))
                if steps:
                    success += [(vx, vy)]
        return success


r = Range.parse(target)
print(f"Result 1: {r.highest_launch_metrics()}")
print(f"Result 2: {len(r.successful_launch_metrics())}")

with open("day17.txt") as f:
    r = Range.parse(f.read())
print(f"Result 1: {r.highest_launch_metrics()}")
print(f"Result 2: {len(r.successful_launch_metrics())}")
