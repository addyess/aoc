import re
from itertools import cycle

START_RE = re.compile(r"Player (?P<player>\d) starting position: (?P<starts>\d+)")

with open("day21-sample.txt") as fin:
    gen = (START_RE.match(line) for line in fin)
    start = {int(m.group("player")): int(m.group("starts")) for m in gen if m}


class DeterministicDice:
    def __init__(self):
        self.dice = cycle(range(1, 101))
        self.rolls = 0

    def __next__(self):
        self.rolls += 1
        return next(self.dice)


def game(dice, _start, final):
    player = 1
    position = dict(_start)
    score = {p: 0 for p in position}
    while all(s < final for s in score.values()):
        steps = sum(next(dice) for _ in range(3))
        position[player] = (steps + position[player]) % 10
        score[player] += position[player] or 10
        player = 2 if player == 1 else 1
    return min(score.values()) * dice.rolls


print(f"Result #1: {game(DeterministicDice(), start, 1000)}")
