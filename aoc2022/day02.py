#! /usr/bin/python3
from aoc.file import example, puzzle_input
from enum import IntEnum
from collections import namedtuple


class Outcome(IntEnum):
    LOSS = 0
    DRAW = 3
    WIN = 6


Shape = IntEnum("Shape", ["ROCK", "PAPER", "SCISSOR"])
Rule = namedtuple("Rule", "them, me, outcome")
RULES = [
    Rule(Shape.ROCK, Shape.ROCK, Outcome.DRAW),
    Rule(Shape.ROCK, Shape.PAPER, Outcome.WIN),
    Rule(Shape.ROCK, Shape.SCISSOR, Outcome.LOSS),
    Rule(Shape.PAPER, Shape.ROCK, Outcome.LOSS),
    Rule(Shape.PAPER, Shape.PAPER, Outcome.DRAW),
    Rule(Shape.PAPER, Shape.SCISSOR, Outcome.WIN),
    Rule(Shape.SCISSOR, Shape.ROCK, Outcome.WIN),
    Rule(Shape.SCISSOR, Shape.PAPER, Outcome.LOSS),
    Rule(Shape.SCISSOR, Shape.SCISSOR, Outcome.DRAW),
]
OPPONENT = {"A": Shape.ROCK, "B": Shape.PAPER, "C": Shape.SCISSOR}
ASSUMPTION = {"X": Shape.ROCK, "Y": Shape.PAPER, "Z": Shape.SCISSOR}
OUTCOME = {"X": Outcome.LOSS, "Y": Outcome.DRAW, "Z": Outcome.WIN}


def strategy(lines):
    def play_for_outcome(theirs: Shape, outcome: Outcome) -> Shape:
        moves = {(r.them, r.outcome): r.me for r in RULES}
        return moves[(theirs, outcome)]

    def score_round(theirs: Shape, mine: Shape) -> int:
        outcomes = {(r.them, r.me): r.outcome for r in RULES}
        return outcomes[(theirs, mine)] + mine

    score_1, score_2 = 0, 0
    for line in lines:
        _1, _2 = line.split()

        theirs, mine = OPPONENT[_1], ASSUMPTION[_2]
        score_1 += score_round(theirs, mine)

        outcome = OUTCOME[_2]
        mine = play_for_outcome(theirs, outcome)
        score_2 += score_round(theirs, mine)
    return score_1, score_2


res_1, res_2 = strategy(example("""A Y\nB X\nC Z"""))
assert res_1 == 15
assert res_2 == 12

res_1, res_2 = strategy(puzzle_input())
print(f"Result 1: {res_1}")
print(f"Result 2: {res_2}")
