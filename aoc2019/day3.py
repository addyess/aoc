with open("day3.txt") as fin:
    ins = [
        _.strip().split(",")
        for _ in fin.readlines()
    ]


class Wire:
    def __init__(self, points):
        self.points = points

    def intersections(self, wire):
        p = list(self.points.keys() & wire.points.keys())
        p.sort(key=lambda _: abs(_[0]) + abs(_[1]))
        return p

    def shortest_cross(self, crosspoints, wire):
        return min([self.points[_] + wire.points[_] for _ in crosspoints])

    @classmethod
    def from_path(cls, path, start=None):
        x, y = start or (0, 0)
        inc = {
            "U": (0, 1), "D": (0, -1), "R": (1, 0), "L": (-1, 0)
        }
        points = {}
        step_count = 0
        for step in path:
            step_dir, step_len = step[0], int(step[1:])
            dx, dy = inc[step_dir]
            for _ in range(step_len):
                step_count += 1
                point = x+dx, y+dy
                points[point] = step_count
                x, y = point
        return cls(points)


w1 = Wire.from_path(ins[0])
w2 = Wire.from_path(ins[1])

crosspaths = w1.intersections(w2)
min_x, min_y = crosspaths[0]
orig_dist = abs(min_x) + abs(min_y)
print(f"Result 1: {orig_dist}")

comb_path = w1.shortest_cross(crosspaths, w2)
print(f"Result 2: {comb_path}")
