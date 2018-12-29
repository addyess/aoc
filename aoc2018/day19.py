from day16 import Registers
import six.moves
import re
import logging
logging.basicConfig(filename='log19.txt', filemode='w',
                    format='%(asctime)-15s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
bind = re.compile(r'#ip (\d+)')


def execute(instructions, regs):
    bound_reg, ip = None, 0
    bound = bind.match(instructions[0])
    if bound:
        bound_reg = next(six.moves.map(int, bound.groups()))

    def compiler(inst_text):
        opcode, a, b, c = inst_text.split()
        opcode = regs.as_index(opcode)
        return list(map(int, (opcode, a, b, c))) + [inst_text]

    inc_pr = compiler('addi %d 1 %d' % (bound_reg, bound_reg))[:-1]
    instructions = list(six.moves.map(compiler, instructions[1:]))
    while ip != len(instructions):
        pre_ip, pre_regs = ip, regs
        if 0 <= ip <= len(instructions):
            opcode, a, b, c, inst_text = instructions[ip]
        else:
            raise StopIteration("ip={} is out of bounds", ip)

        regs = regs.execute(opcode, a, b, c)
        yield pre_ip, pre_regs.regs, inst_text, regs.regs
        if bound_reg is not None:
            regs = regs.execute(*inc_pr)
            ip = regs.regs[bound_reg]
        else:
            ip += 1


def emulate(instructions, next_regs):
    count = 0
    for ip, regs, inst, next_regs in execute(instructions, next_regs):
        logger.info('ip=%s %s %s %s', ip, regs, inst, next_regs)
        count += 1
    return next_regs, count


def sum_factors_of(x):
    sum = 0
    for i in range(1, x + 1):
        if x % i == 0:
            sum += i
    return sum


def main():
    logger.info("Start")
    with open('input19.txt') as in_file:
        instructions = [l.strip() for l in in_file if l.strip()]
    regs, _ = emulate(instructions, Registers(0, *[0]*5))
    logger.info("Solution #1: %d", regs[0])

    for ip, regs, inst, next_regs in execute(instructions, Registers(1, *[0]*5)):
        if next_regs[2] == 0:
            break

    logger.info("Solution #2: %d", sum_factors_of(next_regs[1]))


if __name__ == '__main__':
    main()
