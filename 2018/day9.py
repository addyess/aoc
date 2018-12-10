import logging
from itertools import imap
import blist
import re

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)-15s: %(message)s', level=logging.INFO)
logger.info("Start")
parse_re = re.compile(r"(\d+) players; last marble is worth (\d+) points: high score is (\d+)")


class Game:
    @classmethod
    def make(cls, line):
        return Game(parse_re.search(line.strip()).groups())

    def __init__(self, args):
        self.players, self.marbles, self.score = imap(int, args)
        self.cur_pos = 0
        self.loop = blist.blist()
        self.loop.insert(0, 0)
        self.loop_len = 1
        self.scores = [0] * self.players

    def player(self, value):
        return value % self.players

    def next_id(self):
        return (self.cur_pos + 1) % self.loop_len + 1

    def back(self):
        return (self.cur_pos + self.loop_len - 7) % self.loop_len

    def place(self, value):
        if value % 23 != 0:
            self.cur_pos = self.next_id()
            self.loop.insert(self.cur_pos, value)
            self.loop_len += 1
        else:
            player = self.player(value)
            self.cur_pos = self.back()
            removed = self.loop.pop(self.cur_pos)
            self.loop_len -= 1
            self.scores[player] += value + removed

    def sol1(self):
        for v in range(0, int(self.marbles)):
            self.place(v+1)
        return max(self.scores)


def main():
    with open('input9.txt') as f:
        games = [Game.make(l) for l in f if not l.startswith('#')]

    for game in games:
        if game.score:
            assert game.sol1() == game.score
        else:
            logger.info('Solution #1 %d', game.sol1())

main()