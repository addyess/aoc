from functools import reduce
from math import prod
with open("day18.txt") as f_in:
    ins = [_.strip() for _ in f_in]


class NewMath:
    def __init__(self, text_it):
        self.text = text_it

    def terms(self, prop):
        acc = ""
        for c in self.text:
            if c == "(":
                acc += str(getattr(NewMath(self.text), prop))
                yield acc
                acc = ""
            elif c == ")":
                yield acc
                return
            elif c in "*+":
                if acc:
                    yield acc
                acc = c
            else:
                acc += c.strip()
        yield acc

    @property
    def value(self):
        def merge(acc, term):
            if term.startswith("+"):
                acc += int(term[1:])
            elif term.startswith('*'):
                acc *= int(term[1:])
            elif term:
                acc = int(term)
            return acc
        return reduce(merge, self.terms('value'), 0)

    @property
    def advanced(self):
        stack = []
        for term in self.terms('advanced'):
            if term.startswith("+"):
                stack[-1] += int(term[1:])
            elif term.startswith("*"):
                stack.append(int(term[1:]))
            elif term:
                stack.append(int(term))
        return prod(stack)


print(f"Result 1: {sum(NewMath(iter(line)).value for line in ins)}")
print(f"Result 2: {sum(NewMath(iter(line)).advanced for line in ins)}")
