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


def lcg(lines, m, n, pos):
    def combine(f, unit, a, b):
        r = unit
        while True:
            if not b: return r
            if b & 1: r = f(r, a)
            b >>= 1
            a = f(a, a)

    add = lambda a, b: ((m + (a + b) % m) % m)
    mul = lambda a, b: combine(add, 0, a, b)
    pow = lambda a, b: combine(mul, 1, a, b)
    k, b, x = 1, 0, None
    for s in lines:
        if "inc" in s:
            x = int(s.split("increment ")[-1])
            k = mul(k, x)
            b = mul(b, x)
        elif "cut" in s:
            x = int(s.split("cut ")[-1])
            b = add(b, -x)
        elif "new" in s:
            k = add(0, -k)
            b = add(-1, -b)
    x = mul(b, pow(k - 1, m - 2))
    return add(mul(add(x, pos), pow(pow(k, m - 2), n)), -x)


def main():
    with open("day22.txt") as fin:
        ins = fin.read()
    lines = ins.splitlines()

    stack = Stack.operate(lines, Stack(range(0, 10007)))
    print(f"Result 1: {list(stack.cards).index(2019)}")

    val = lcg(lines, 119315717514047, 101741582076661, 2020)
    print(f"Result 2: {val}")


if __name__ == '__main__':
    main()
