from day19 import execute
from day16 import Registers
import logging
logging.basicConfig(format='%(asctime)-15s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


def emulate(instructions, next_regs, ips=[28]):
    inscount = 0
    for ip, regs, inst, next_regs in execute(instructions, next_regs):
        if ip in ips:
            logger.info("pc=(%d) regs(%s)", ip, map(hex, regs))
        if ip == 28:
            yield regs[5], inscount
        inscount += 1


def main():
    logger.info("Start")
    with open('input21.txt') as in_file:
        instructions = [l.strip() for l in in_file if l.strip()]
    reg_5, _ = next(emulate(instructions, Registers(0, *[0]*5)))
    logger.info("Solution #1: %d(%s)", reg_5, hex(reg_5))

    reg_5_options = {}
    for reg_5, ins in emulate(instructions, Registers(0, *[0]*5), ips=[]):
        if reg_5 not in reg_5_options:
            reg_5_options[reg_5] = ins
        else:
            break

    import operator
    longest = sorted(reg_5_options.items(), key=operator.itemgetter(1), reverse=True)
    reg_5, _= longest[0]
    logger.info("Solution #2: %d(%s)", reg_5, hex(reg_5))


if __name__ == '__main__':
    main()
