import re
from itertools import cycle

START_RE = re.compile(r"Player (?P<player>\d) starting position: (?P<starts>\d+)")

with open("day21.txt") as fin:
    gen = (START_RE.match(line) for line in fin)
    start = {int(m.group("player")): int(m.group("starts")) for m in gen if m}


class GameState:
    def __init__(self, _start, _high_score):
        self.position = dict(_start)
        self.high_score = _high_score
        self.player = 1
        self.score = {p: 0 for p in self.position}
        self.rolls = 0

    @property
    def winner(self):
        return next(
            iter(p for p, s in self.score.items() if s >= self.high_score), None
        )

    @property
    def non_player(self):
        return 2 if self.player == 1 else 1

    def split_universe(self):
        g = GameState(self.position, self.high_score)
        g.player = self.non_player
        g.score = dict(self.score)
        g.rolls = self.rolls
        return g


def deterministic_game(state):
    winner, dice = state.winner, cycle(range(1, 101))
    while not winner:
        steps = sum(next(dice) for _ in range(3))
        state.rolls += 3
        state.position[state.player] = (steps + state.position[state.player]) % 10
        state.score[state.player] += state.position[state.player] or 10
        state.player = state.non_player
        winner = state.winner
    return min(state.score.values()) * state.rolls


def dirac_games(state, mult):
    winner, player = state.winner, state.player
    if not winner:
        state.rolls += 3
        counts = {p: 0 for p in state.position}
        for steps, universes in dirac_probability.items():
            new_state = state.split_universe()
            new_state.position[player] = (steps + new_state.position[player]) % 10
            new_state.score[player] += new_state.position[player] or 10
            counts = {
                p: wins + counts[p]
                for p, wins in dirac_games(new_state, mult * universes).items()
            }
        return counts
    else:
        return {player: 1 * mult, state.non_player: 0}


dirac_probability = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1,
}
print(f"Result #1: {deterministic_game(GameState(start, 1000))}")
all_wins = dirac_games(GameState(start, 21), 1)
print(f"Result #2: {max(all_wins.values())}")
