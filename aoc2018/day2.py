import six
import logging
logger = logging.getLogger(__name__)

FORMAT = '%(asctime)-15s: %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger.info("Start")


class IdCode(str):
    def __init__(self, code):
        super(IdCode, self).__init__(code)

    def counts_as_2_and_3(self):
        d, as_2, as_3 = {}, False, False
        for letter in self:
            try:
                d[letter] += 1
            except KeyError:
                d[letter] = 1
        for letter, count in six.iteritems(d):
            if count == 2:
                as_2 = True
            if count == 3:
                as_3 = True
        return as_2, as_3

    def diff_with(self, code):
        diff, shortened = 0, ''
        for l1, l2 in zip(self, code):
            diff += l1 != l2
            if diff > 1:
                break
            if l1 == l2:
                shortened += l1
        return diff, shortened


with open('input2.txt') as f:
    codes = [IdCode(ln.strip()) for ln in f.readlines() if ln]


exact_2s = 0
exact_3s = 0
for item in codes:
    t = item.counts_as_2_and_3()
    exact_2s += t[0]
    exact_3s += t[1]
logger.info("%s x %s = %d", exact_2s, exact_3s, exact_3s * exact_2s)


def identify_close():
    for i, cmp1 in enumerate(codes):  # [0..n]
        for cmp2 in codes[i+1:]:      # [i+1..n]
            diff, shortened = cmp1.diff_with(cmp2)
            if diff == 1:
                return shortened


logger.info("Share the same letters %s", identify_close())
