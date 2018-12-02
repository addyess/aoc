import logging
import time
logger = logging.getLogger(__name__)

FORMAT = '%(asctime)-15s: %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger.info("Start")
with open('input1.txt') as f:
	ints = [int(i) for i in f.readlines() if i]

logger.info("Solution #1 (%d)", sum(ints))

solution = None
current = 0
memory = {0}
while not solution:
    for a in ints:
        current += a
        if current in memory:
            solution = current
            break
        memory.add(current)
logger.info("Solution #2 (%d)", solution)

