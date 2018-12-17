import string
import logging
import re
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)-15s: %(message)s', level=logging.INFO)
logger.info("Start")
with open('input5.txt') as f:
    polymer = f.read().strip()


def scan(accum, cur):
    if accum:
        prev = accum[-1]
        if prev.upper() == cur.upper() and cur != prev:
            return accum[:-1]
    return accum + cur


def chain_length(chain): return len(reduce(scan, chain))


def is_shorter(accum, letter):
    replaced = re.sub(r'[{}{}]'.format(letter, letter.upper()), '', polymer)
    return min(accum, chain_length(replaced))


logger.info("Solution #1 - %d", chain_length(polymer))
logger.info("Solution #2 - %d", reduce(is_shorter, string.ascii_lowercase, len(polymer)))
