from collections import deque
from itertools import count
VERBOSE = False

with open("day22.txt") as f_in:
    ins = f_in.read()

class Deck:
    @classmethod
    def parse(cls, sections):
        for idx, section in enumerate(sections):
            yield cls(idx + 1, section.strip().splitlines()[1:])

    @classmethod
    def cp(cls, deck, n):
        return cls(deck.pid, list(deck.data)[0:n])

    def __repr__(self):
        return f"Deck {self.pid}"

    def __init__(self, pid, lines):
        self.pid = pid
        self.data = deque(int(l) for l in lines)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.data.popleft()
        except IndexError:
            raise StopIteration

    def win(self, cards):
        for c in cards:
            self.data.append(c)


def verbose(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)


def score(p):
    return sum((idx + 1) * c for idx, c in enumerate(reversed(p.data)))


def combat(text):
    p1, p2 = Deck.parse(text)
    for round, (c1, c2) in enumerate(zip(p1, p2)):
        m = max(c1, c2)
        verbose(f" -- Round {round + 1} --")
        verbose(f" Player 1 plays {c1}")
        verbose(f" Player 2 plays {c2}")
        w = p1 if m == c1 else p2
        verbose(f" Player {w.pid} wins the round!")
        order = (c1, c2) if p1 == w else (c2, c1)
        w.win(order)
    w = p1 if len(p1.data) else p2
    return score(w)


def rcombat(text):
    def game(p1_init, p2_init, gid):
        _p1, _p2 = Deck.cp(*p1_init), Deck.cp(*p2_init)
        history = set()
        verbose(f"=== Game {gid} ===")
        verbose()
        for round, (c1, c2) in enumerate(zip(_p1, _p2)):
            verbose(f" -- Round {round + 1} (Game {gid}) --")
            verbose(f" Player 1's deck {[c1] + list(_p1.data)}")
            verbose(f" Player 2's deck {[c2] + list(_p2.data)}")
            verbose(f" Player 1 plays {c1}")
            verbose(f" Player 2 plays {c2}")
            if all(len(p.data) >= c for p, c in zip((_p1, _p2), (c1, c2))):
                # enough to recurse
                verbose(" Playing a sub-game to determine the winner...")
                verbose()
                wid, _ = game((_p1, c1), (_p2, c2), next(gids))
                w = _p1 if _p1.pid == wid else _p2
                verbose(f"...anyway, back to game {gid}")
            else:
                m = max(c1, c2)
                w = _p1 if m == c1 else _p2
            verbose(f" Player {w.pid} wins round {round + 1} of game {gid}!")
            order = (c1, c2) if _p1 == w else (c2, c1)
            w.win(order)
            verbose()
            hash = (tuple(_p1.data), tuple(_p2.data))
            if hash in history:
                return 1, score(_p1) if gid == 1 else None
            history.add(hash)

        wid = _p1.pid if len(_p1.data) else _p2.pid
        ws = None
        if gid == 1:
            ws = score(_p1 if wid == _p1.pid else _p2)
        return wid, ws

    gids = count(1)
    p1, p2 = Deck.parse(text)
    wid, ws = game((p1, len(p1.data)), (p2, len(p2.data)), next(gids))
    return ws

players_text = ins.split("\n\n")
print(f"Result 1: {combat(players_text)}")
print(f"Result 2: {rcombat(players_text)}")
