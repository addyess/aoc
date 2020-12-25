import re

with open("day19.txt") as f_in:
    ins = f_in.read()


class Rules:
    def __init__(self, lines):
        def key_pair(line):
            head, tail = line.split(":")
            value = tail.replace('"', '')
            if '|' in value:
                value = "(?: " + value + " )"
            return head, value.split()

        self.tree = dict(map(key_pair, lines.splitlines()))

    @property
    def part1_re(self):
        pattern = self.tree['0']
        while any(x.isdigit() for x in pattern):
            i, k = next((i, k) for i, k in enumerate(pattern) if k.isdigit())
            pattern[i:i + 1] = self.tree[k]
        pattern.insert(0, '^')
        pattern.append('$')
        return re.compile(''.join(pattern))

    @property
    def part2_re(self):
        rules.tree['8'] = "(?: 42 )+".split()  # 1 or more 42s
        rules.tree['11'] = (
            "(?: "
            "(?: (?: 42 ) {1} (?: 31 ) {1} ) "  # 1 42 and 1 31 ...
            "| (?: (?: 42 ) {2} (?: 31 ) {2} ) "  # or 2 42 and 2 31 ...
            "| (?: (?: 42 ) {3} (?: 31 ) {3} ) "  # or 3 42 and 3 31 ...
            "| (?: (?: 42 ) {4} (?: 31 ) {4} ) "  # or 4 42 and 4 31 ...
            # "| (?: (?: 42 ) {5} (?: 31 ) {5} ) "   # adding more made no difference...
            ")"
        ).split()
        return self.part1_re


rules_txt, messages = ins.split("\n\n")
rules = Rules(rules_txt)
total = sum(bool(rules.part1_re.match(txt)) for txt in messages.splitlines())
print(f"Result 1: {total}")

rules = Rules(rules_txt)
total = sum(bool(rules.part2_re.match(txt)) for txt in messages.splitlines())
print(f"Result 2: {total}")
