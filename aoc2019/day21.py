try:
    from aoc2019.computer import Machine
except ImportError:
    from computer import Machine


class SystemComplete(BaseException):
    pass


class Terminal:
    PROMPT = ""

    def __init__(self, system):
        self.system = system
        self.before = ''
        self.line = ''

    def __iter__(self):
        return self

    def __next__(self):
        if not self.line:
            before, self.before = self.before, ''
            self.line = self.system.next() + "\n"
        h, self.line = self.line[0], self.line[1:]
        return ord(h)

    def send(self, val):
        if 0 <= val <= 127:
            self.before += chr(val)
            return
        raise SystemComplete(val)


class System:
    def __init__(self, command_blocks, exec):
        self.terminal = Terminal(self)
        self.exec = exec
        self.commands = []
        self.used_blocks, self.command_blocks = 0, command_blocks

    def next(self):
        if not self.commands:
            self.commands = self.next_block()
        h, self.commands = self.commands[0], self.commands[1:]
        return h

    def next_block(self):
        block, self.command_blocks = self.command_blocks[0], self.command_blocks[1:]
        self.used_blocks += 1
        return list(filter(None, block.split(";") + [self.exec]))


def main():
    with open("day21.txt") as fin:
        ins = fin.read()

    """
    NOT(A&B&C) & D
    if there's a D landing spot, with any missing spot in front, take a leap
    """
    sys = System(["NOT J J;AND A J;AND B J;AND C J;NOT J J;AND D J;"], "WALK")
    machine = Machine.decode(ins, sys.terminal, sys.terminal)
    try:
        machine.run()
        print(sys.terminal.before)
    except SystemComplete as e:
        print(f"Result 1: {e}")

    """
    Take a leap to D if there's any missing from A,B,C - AND - E or H is available for the next jump or move
    ALWAYS leap if E,F & G are all washed out -- trust me
    ( (E|H) & NOT(A & B &C) & D ) | NOT(E|F|G)
    """

    sys = System(["OR H T;OR E T;NOT J J;AND A J;AND B J;AND C J;NOT J J;AND T J;AND D J;OR F T;OR G T;NOT T T;OR T J;"], "RUN")
    machine = Machine.decode(ins, sys.terminal, sys.terminal)
    try:
        machine.run()
        print(sys.terminal.before)
    except SystemComplete as e:
        print(f"Result 2: {e}")


main()
