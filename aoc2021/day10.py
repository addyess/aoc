from statistics import median


class Syntax:
    class CorruptError(Exception):
        pass

    PAIR = {"(": ")", "[": "]", "{": "}", "<": ">"}
    CORRUPT = {")": 3, "]": 57, "}": 1197, ">": 25137}
    AUTOCOMPLETE = {")": 1, "]": 2, "}": 3, ">": 4}

    def __init__(self, lines):
        self.lines = [_.strip() for _ in lines]
        self.corrupted = [_ for _ in map(self.corrupt_score, self.lines) if _]
        self.complete = [_ for _ in map(self.incomplete_score, self.lines) if _]

    def corrupt_score(self, line):
        try:
            self.find_chunk(line)
        except self.CorruptError as c:
            return self.CORRUPT[str(c)]
        return 0

    def incomplete_score(self, line):
        def score(score_me):
            total = 0
            for c in score_me:
                total = total * 5 + self.AUTOCOMPLETE[c]
            return total

        try:
            additions, _ = self.find_chunk(line)
        except self.CorruptError:
            return None
        return score(additions)

    def find_chunk(self, search):
        opening, *tail = search
        additions = ""
        while tail:
            head, *tail = tail
            if self.PAIR[opening] == head:
                if tail and tail[0] in self.PAIR:
                    return self.find_chunk(tail)
                return additions, tail
            if head in self.PAIR:
                to_add, tail = self.find_chunk([head] + tail)
                additions += to_add
            else:
                raise self.CorruptError(head)
        return additions + self.PAIR[opening], ""


with open("day10.txt") as fin:
    navsystem = Syntax(fin)
res1 = navsystem.corrupted
print(f"Result 1: {sum(res1)}")
res2 = navsystem.complete
print(f"Result 2: {median(res2)}")
