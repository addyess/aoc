from itertools import combinations
try:
    from aoc2019.computer import Machine
except ImportError:
    from computer import Machine


class SystemComplete(BaseException):
    pass


class Terminal:
    PROMPT = ""

    def __init__(self, system):
        self.system = iter(system)
        self.before = ''
        self.line = ''

    def __iter__(self):
        return self

    def __next__(self):
        if not self.line:
            before, self.before = self.before, ''
            print(before.strip())
            self.line = next(self.system) + "\n"
        h, self.line = self.line[0], self.line[1:]
        return ord(h)

    def send(self, val):
        if 0 <= val <= 127:
            self.before += chr(val)
            return
        raise SystemComplete(val)


class System:
    def __init__(self):
        self.terminal = Terminal(self)
        self.items = [
            "hologram",
            "food ration",
            "space law space brochure",
            "cake",
            "astrolabe",
            "wreath",
            "coin",
            "hypercube"
        ]
        self.held = []
        self.dropped = []

    def __iter__(self):
        while True:
            command = input()
            if command == 'perm':
                break
            yield command
        choices = self.options()
        while True:
            yield "south"
            for item in self.items:
                yield f"drop {item}"
            choice = next(choices)
            for item in choice:
                yield f"take {item}"

    def options(self):
        num_items = len(self.items)
        for n in range(num_items+1):
            for _ in combinations(self.items, num_items - n):
                yield _


def main():
    with open("day25.txt") as fin:
        ins = fin.read()

    sys = System()
    machine = Machine.decode(ins, sys.terminal, sys.terminal)
    try:
        machine.run()
        print(sys.terminal.before)
    except SystemComplete as e:
        print(f"Result 1: {e}")


main()
