import logging
from itertools import cycle
logger = logging.getLogger(__name__)

FORMAT = '%(asctime)-15s: %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger.info("Start")
with open('input1.txt') as f:
    ints = [int(i) for i in f.readlines() if i]

logger.info("Solution #1 (%d)", sum(ints))

current = 0
memory = {0}
for i in cycle(ints):
    current += i
    if current in memory:
        logger.info("Solution #2 (%d)", current)
        break
    memory.add(current)

