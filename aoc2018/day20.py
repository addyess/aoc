import logging
from itertools import takewhile
import re

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)-15s: %(message)s', level=logging.INFO)


def end_of_group(p_count):
    def fn(x):
        if x == '(':
            s[0] += 1
        elif x == ')':
            s[0] -= 1
        else:
            return True
        return s[0] != 0
    s = {0: p_count}
    return fn


class HQMap:
    def __init__(self, regex=''):
        regex = re.sub(r'\(\w{4}\|\)', '', regex)
        self.regex = regex\
            .replace('^', '')\
            .replace('$', '')

    def group(self):
        it = iter(self.regex)
        pre = ''.join(takewhile(lambda _: _ not in '(', it)).split('|')
        run = ''.join(takewhile(end_of_group(1), it))
        post = ''.join(it).split('|', 1)
        if len(pre) > 1:
            run = pre[1] + '(' + run + ')' + post[0]
            return max(map(len,(HQMap(pre[0]), HQMap(run))))
        if len(post) > 1:
            run = pre[0] + '(' + run + ')' + post[0]
            return max(map(len,(HQMap(run), HQMap(post[1]))))
        return sum(map(len,(HQMap(pre[0]), HQMap(run), HQMap(post[-1]))))

    def __len__(self):
        if '(' in self.regex:
            return self.group()
        elif '|' not in self.regex:
            return len(self.regex)
        return max(map(len, map(HQMap, self.regex.split('|'))))


if __name__ == '__main__':
    logger.info("Start")
    hq = HQMap("^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$")
    assert len(hq) == 23
    hq = HQMap('^WNE$')
    assert len(hq) == 3
    hq = HQMap('^ENWWW(NEEE|SSE(EE|N))$')
    assert len(hq) == 10
    hq = HQMap('^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$')
    assert len(hq) == 18

    with open('input20.txt') as in_file:
        hq = HQMap(regex=in_file.read().strip())
    logger.info("Solution #1: %d", len(hq))
