def manhattan(point):
    return abs(point[0]) + abs(point[1])


class Wire:
    def __init__(self, points):
        self.points = points

    def intersections(self, wire):
        p = list(self.points.keys() & wire.points.keys())
        p.sort(key=manhattan)
        return p

    def shortest_cross(self, x_points, wire):
        return min([self.points[_] + wire.points[_] for _ in x_points])

    @classmethod
    def from_path(cls, path):
        inc = {"U": (0, 1), "D": (0, -1), "R": (1, 0), "L": (-1, 0)}
        points = {}
        point = 0, 0
        step_count = 0
        for step in path:
            step_dir, step_len = step[0], int(step[1:])
            dx, dy = inc[step_dir]
            for _ in range(step_len):
                step_count += 1
                point = point[0]+dx, point[1]+dy
                points[point] = step_count
        return cls(points)


if __name__ == '__main__':
    with open("day3.txt") as fin:
        ins = [
            _.strip().split(",")
            for _ in fin.readlines()
        ]
    w1 = Wire.from_path(ins[0])
    w2 = Wire.from_path(ins[1])
    _x_points = w1.intersections(w2)
    orig_dist = manhattan(_x_points[0])
    print(f"Result 1: {orig_dist}")

    comb_path = w1.shortest_cross(_x_points, w2)
    print(f"Result 2: {comb_path}")
