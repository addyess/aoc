from itertools import chain, cycle, islice

class Stack:
    OP_INC = "deal with increment "
    OP_NEW = "deal into new stack"
    OP_CUT = "cut "

    @staticmethod
    def operate(lines, stack):
        for line in lines:
            if line.startswith(Stack.OP_CUT):
                stack = stack.deal_cut(int(line.split(Stack.OP_CUT)[-1]))
            elif line.startswith(Stack.OP_NEW):
                stack = stack.deal_new()
            elif line.startswith(Stack.OP_INC):
                stack = stack.deal_inc(int(line.split(Stack.OP_INC)[-1]))
        return stack

    def __init__(self, cards):
        self.cards = list(cards)

    def deal_new(self):
        return Stack(reversed(self.cards))

    def deal_cut(self, n):
        return Stack(self.cards[n:] + self.cards[:n])

    def deal_inc(self, i):
        cards = len(self.cards)
        target = [None] * cards
        for idx, card in enumerate(self.cards):
            target[(idx * i) % cards] = card
        return Stack(target)

    def deal_inc2(self, i):
        return Stack(chain(
            [self.cards[0]],
            islice(
                islice(cycle(self.cards), i+1, None, i+1),
                0, len(self.cards)-1)))


def main():
    with open("day22.txt") as fin:
        ins = fin.read()
    lines = ins.splitlines()

    stack = Stack.operate(lines, Stack(range(0, 10007)))
    print(f"Result 1: {list(stack.cards).index(2019)}")

    stack = Stack(range(0, 83))
    for _ in range(0, 83):
        stack = stack.operate(lines, stack)

    stack = Stack(range(0, 119315717514047))
    for _ in range(0, 101741582076661):
        stack = Stack.operate(lines, stack)
    print(f"Result 2: {list(stack.cards)[2020]}")


if __name__ == '__main__':
    main()
