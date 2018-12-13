import logging
from collections import namedtuple

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)-15s: %(message)s', level=logging.INFO)
Cart = namedtuple('Cart', ['dir', 'next_turn'])


class Map:
    DIRECTIONS = '^>v<'

    @classmethod
    def create(cls, txt):
        carts = {}
        tracks = []
        for y, row in enumerate(txt):
            track_row = []
            tracks.append(track_row)
            for x, char in enumerate(row):
                if char in cls.DIRECTIONS:
                    carts[y, x] = Cart(char, -1)
                    char = '-' if char in '<>' else '|'
                track_row.append(char)
        return cls(tracks, carts)

    def __init__(self, tracks, carts):
        self.carts = carts
        self.tracks = tracks

    @staticmethod
    def intersect(cart):
        next_turn = cart.next_turn
        next_dir = Map.DIRECTIONS[
            (Map.DIRECTIONS.index(cart.dir) + next_turn) % len(Map.DIRECTIONS)
            ]
        return next_dir, ((next_turn - 1) % 3) - 1

    def tick(self):
        vector = {
            '>': lambda (y, x): (y, x + 1),
            '<': lambda (y, x): (y, x - 1),
            'v': lambda (y, x): (y + 1, x),
            '^': lambda (y, x): (y - 1, x),
        }
        collisions = []
        carts = self.carts.copy()
        for (cart_y, cart_x) in sorted(carts.keys()):
            cart = carts.pop((cart_y, cart_x), None)
            if not cart:
                continue

            y, x = vector[cart.dir]((cart_y, cart_x))
            t = self.tracks[y][x]

            if cart.dir == '>':
                dir = '>' if t == '-' else \
                    '^' if t == '/' else \
                        'v' if t == '\\' else None
            elif cart.dir == '<':
                dir = '<' if t == '-' else \
                    'v' if t == '/' else \
                        '^' if t == '\\' else None
            elif cart.dir == 'v':
                dir = 'v' if t == '|' else \
                    '<' if t == '/' else \
                        '>' if t == '\\' else None
            else:
                dir = '^' if t == '|' else \
                    '>' if t == '/' else \
                        '<' if t == '\\' else None
            dir, next_turn = self.intersect(cart) if dir is None else (dir, cart.next_turn)
            collides = carts.pop((y, x), None)
            if collides:
                collisions.append((x, y))
            else:
                carts[y, x] = Cart(dir, next_turn)
        return Map(self.tracks, carts), collisions

    def first_collision(self):
        stage = self
        collisions = []
        while not collisions:
            stage, collisions = stage.tick()
        return collisions

    def remove_collision(self):
        stage = self
        while len(stage.carts) > 1:
            stage, _ = stage.tick()
        y, x = stage.carts.keys()[0]
        return x, y


def main():
    test = r'''
/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   '''.strip().split('\n')
    m = Map.create(test)
    assert m.first_collision() == [(7, 3)]

    test = r'''
/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/'''.strip().split('\n')
    m = Map.create(test)
    assert m.remove_collision() == (6, 4)

    test = r'''
/><-\  
|   |  
| /-+-\
| | | |
\-+-/ |
  |   |
  \---/'''.strip().split('\n')
    m = Map.create(test)
    assert m.first_collision() == [(2, 0)]

    logger.info("Start")
    with open('input13.txt') as in_file:
        m = Map.create(in_file.readlines())

    sol1, sol2 = m.first_collision(), m.remove_collision()
    logger.info('Solution #1: %s', sol1)
    logger.info('Solution #2: %s', sol2)


main()
