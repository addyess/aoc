from collections import namedtuple
import six
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)-15s: %(message)s', level=logging.INFO)
Result = namedtuple('Result', 'func, match')


class Registers:
    def __init__(self, *args):
        self.regs = args
        self.methods = [
            'addr', 'addi', 'mulr', 'muli',
            'banr', 'bani', 'borr', 'bori',
            'setr', 'seti', 'gtir', 'gtri',
            'gtrr', 'eqir', 'eqri', 'eqrr'
        ]

    def __eq__(self, other):
        return self.regs == other.regs

    def as_index(self, opcode):
        if isinstance(opcode, six.string_types):
            return self.methods.index(opcode)
        return opcode

    def execute(self, opcode, a, b, c):
        regs = list(self.regs)
        opcode = self.as_index(opcode)
        if opcode == 0:
            regs[c] = self.regs[a] + self.regs[b]
        elif opcode == 1:
            regs[c] = self.regs[a] + b
        elif opcode == 2:
            regs[c] = self.regs[a] * self.regs[b]
        elif opcode == 3:
            regs[c] = self.regs[a] * b
        elif opcode == 4:
            regs[c] = self.regs[a] & self.regs[b]
        elif opcode == 5:
            regs[c] = self.regs[a] & b
        elif opcode == 6:
            regs[c] = self.regs[a] | self.regs[b]
        elif opcode == 7:
            regs[c] = self.regs[a] | b
        elif opcode == 8:
            regs[c] = self.regs[a]
        elif opcode == 9:
            regs[c] = a
        elif opcode == 10:
            regs[c] = 1 if a > self.regs[b] else 0
        elif opcode == 11:
            regs[c] = 1 if self.regs[a] > b else 0
        elif opcode == 12:
            regs[c] = 1 if self.regs[a] > self.regs[b] else 0
        elif opcode == 13:
            regs[c] = 1 if a == self.regs[b] else 0
        elif opcode == 14:
            regs[c] = 1 if self.regs[a] == b else 0
        elif opcode == 15:
            regs[c] = 1 if self.regs[a] == self.regs[b] else 0
        return Registers(*regs)


def evaluate(_before, _after, ins):
    before = Registers(*_before)
    after = Registers(*_after)
    opc, a, b, c = ins
    result = set(Result(fn, after == before.execute(fn, a, b, c)) for fn in before.methods)
    return opc, result


def get_opcodes():
    matches = 0
    with open('input16.txt') as in_file:
        ins, before, after = '', '', ''
        blank_lines = 0
        opcode_map = {}

        for l in in_file:
            l = l.strip()
            before = l.strip('Before: ') if l.startswith('B') else before
            ins = l.strip() if not (l.startswith('A') or l.startswith('B')) else ins
            after = l.strip('After:  ') if l.startswith('A') else after

            if before and after and ins:
                opcode, result = evaluate(eval(before), eval(after), map(int, ins.split()))
                after = ''
                true_set = set(r.func for r in result if r.match)
                matches += 1 if len(true_set) >= 3 else 0

                s = opcode_map.get(opcode, true_set)
                opcode_map[opcode] = s.intersection(true_set)

            blank_lines = 0 if l else (blank_lines + 1)
            if blank_lines == 3:
                break
        return matches, opcode_map, list(in_file)


def prune(ops):
    certain = {v for s in ops.values() if len(s) == 1 for v in s}
    if len(certain) == 16:
        return True, {k: op.pop() for k, op in ops.items()}
    for v in ops.values():
        if len(v) != 1:
            v.difference_update(certain)
    return False, ops


def main():
    logger.info("Start")
    m, ops, prog = get_opcodes()
    logger.info("Solution #1: %d", m)
    done = False
    while not done:
        done, ops = prune(ops)
    reg = Registers(0, 0, 0, 0)

    for ins in prog:
        opcode, a, b, c = map(int, ins.split())
        reg = reg.execute(ops[opcode], a, b, c)
    logger.info("Solution #2: %d", reg.regs[0])

if __name__ == '__main__':
    main()
