import logging
from collections import namedtuple

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)-15s: %(message)s', level=logging.INFO)
Cart = namedtuple('Cart', ['sym', 'next_turn'])


class Map:
    DIRECTIONS = '^>v<'
    POS = {
        '>': lambda (y, x): (y, x + 1),
        '<': lambda (y, x): (y, x - 1),
        'v': lambda (y, x): (y + 1, x),
        '^': lambda (y, x): (y - 1, x),
    }
    SYM = {
        '>': {'-': '>', '/': '^', '\\': 'v', '+': None},
        '<': {'-': '<', '/': 'v', '\\': '^', '+': None},
        'v': {'|': 'v', '/': '<', '\\': '>', '+': None},
        '^': {'|': '^', '/': '>', '\\': '<', '+': None},
    }

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
        cur_dir = Map.DIRECTIONS.index(cart.sym)
        next_turn = cart.next_turn
        next_dir = Map.DIRECTIONS[(cur_dir + next_turn) % len(Map.DIRECTIONS)]
        return next_dir, ((next_turn - 1) % 3) - 1

    def tick(self):
        collisions = []
        carts = self.carts.copy()
        for (cart_y, cart_x) in sorted(carts.keys()):         # Move across x axis, then down y
            cart = carts.pop((cart_y, cart_x), None)          # Pickup Cart from Map
            if not cart:                                      # The cart may have collided already
                continue

            y, x = self.POS[cart.sym]((cart_y, cart_x))       # Next Position for Cart
            new_sym = self.SYM[cart.sym][self.tracks[y][x]]   # Next Symbol for Cart
            next_turn = cart.next_turn                        # Next Available Turn for Cart
            if new_sym is None:
                new_sym, next_turn = self.intersect(cart)     # Intersection, Apply turn
            if carts.pop((y, x), None):                       # If there's a cart in new spot
                collisions.append((x, y))                     # Append Collision Location
            else:
                carts[y, x] = Cart(new_sym, next_turn)        # Successfully add cart
        return Map(self.tracks, carts), collisions            # Return new Map and any collisions

    def first_collision(self):
        stage = self
        collisions = []
        while not collisions:
            stage, collisions = stage.tick()
        return collisions[0]

    def remove_collision(self):
        stage = self
        while len(stage.carts) > 1:
            stage, _ = stage.tick()
        y, x = stage.carts.keys()[0]
        return x, y


def main():
    logger.info("Start")
    with open('input13.txt') as in_file:
        m = Map.create(in_file.readlines())
    sol1, sol2 = m.first_collision(), m.remove_collision()
    assert sol1 == (5, 102) and sol2 == (46, 45)
    logger.info('Solution #1: %s', sol1)
    logger.info('Solution #2: %s', sol2)


main()
