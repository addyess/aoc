class Board:
    WINS = [{(x, y) for x in range(5)} for y in range(5)] + [
        {(x, y) for y in range(5)} for x in range(5)
    ]

    @staticmethod
    def order(content):
        return list(map(int, content.split(",")))

    @classmethod
    def all_boards(cls, content):
        def boards():
            last_board = []
            for row in content:
                if row == "\n" and last_board:
                    yield cls(last_board)
                    last_board = []
                else:
                    last_board.append(row)
            if last_board:
                yield cls(last_board)

        return list(boards())

    def __init__(self, grid):
        grid = list(filter(None, (list(map(int, row.strip().split())) for row in grid)))
        self.grid = {
            (r, c): val for r, row in enumerate(grid) for c, val in enumerate(row)
        }
        self.locations = {val: coord for coord, val in self.grid.items()}
        self.matches = set()
        self.complete = False

    def call(self, find_me):
        coord = self.locations.get(find_me)
        if coord:
            self.matches |= {coord}
        if any(win.issubset(self.matches) for win in self.WINS):
            self.complete = True
            return self.unmatched_sum * find_me

    @property
    def unmatched_sum(self):
        unmatched = self.grid.keys() - self.matches
        return sum(self.grid[loc] for loc in unmatched)


def result_1(order, boards):
    for num in order:
        for board in boards:
            if score := board.call(num):
                return score


def result_2(order, boards):
    final_score = 0
    for num in order:
        for board in boards:
            if board.complete:
                continue
            if this_score := board.call(num):
                final_score = this_score
    return final_score


def main():
    with open("day04.txt") as f_in:
        order, *boards = list(f_in)
    print(f"Result 1: {result_1(Board.order(order), Board.all_boards(boards))}")
    print(f"Result 2: {result_2(Board.order(order), Board.all_boards(boards))}")


main()
