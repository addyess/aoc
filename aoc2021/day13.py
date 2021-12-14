class Paper:
    def __init__(self, lines):
        self.dots = set()
        for line in lines:
            line = line.strip()
            if not line:
                break
            self.dots |= {eval(f"({line})")}

        self.fold_order = []
        for line in lines:
            plane, value = line.split("=")
            self.fold_order.append((plane[-1], int(value)))
        self.current = {_ for _ in self.dots}

    def print(self):
        m = max(_ for d in self.current for _ in d)
        for y in range(m + 1):
            line = "".join(
                "@@@" if (x, y) in self.current else "   " for x in range(m + 1)
            )
            if "@" in line:
                print(line)
        print()

    def execute(self):
        for num, (f, row_val) in enumerate(self.fold_order):
            if num == 1:
                print(f"Result 1: {len(self.current)}")
            same, transpose = set(), set()
            for dot in self.current:
                x, y = dot
                dot_val = y if f == "y" else x
                if dot_val > row_val:
                    dist = abs(dot_val - row_val) * 2
                    new_dot = (x - dist if f != "y" else x, y - dist if f == "y" else y)
                    transpose.add(new_dot)
                else:
                    same.add(dot)
            self.current = transpose | same


with open("day13.txt") as fin:
    paper = Paper(fin)
paper.execute()
paper.print()
