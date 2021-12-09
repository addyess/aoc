SEGMENTS = {
    1: set("cf"),
    7: set("acf"),
    4: set("bcdf"),
    2: set("acdeg"),
    3: set("acdfg"),
    5: set("abdfg"),
    6: set("abdefg"),
    0: set("abcefg"),
    9: set("abcdfg"),
    8: set("abcdefg"),
}


def parse(lines):
    for line in lines:
        yield [
            list(map(set, section.split(" ")))
            for section in map(str.strip, line.split("|"))
        ]


def isolate(uniq):
    known = {}
    # these are uniquely identified by number of segments lit
    for num in (1, 4, 7, 8):
        for digit in uniq:
            if len(digit) == len(SEGMENTS[num]):
                known[num] = digit
                uniq.remove(digit)
                break

    # Digit 5 is unique in that the segments in 4 after removing
    # the segments in 1, are unique to the segments in 5 among the
    # digits which have 5 segments lit (2,3,5).
    for digit in uniq:
        if len(digit) == len(SEGMENTS[5]):
            if (known[4] - known[1]).issubset(digit):
                known[5] = digit
                uniq.remove(digit)

    # Of the remaining digits with len == 6,
    # only 6 doesn't have the 1 segments within it (0, 6, 9)
    for digit in uniq:
        if len(digit) == len(SEGMENTS[6]):
            if not known[1].issubset(digit):
                known[6] = digit
                uniq.remove(digit)

    # 9 can be represented by doing set math on 8, 6 & 5
    nine = known[8] - (known[6] - known[5])
    known[9] = nine
    uniq.remove(nine)

    # 0, 2, and 3 are now distinguishable by segment length
    # and whether-or-not 1 is a subset of them
    for digit in uniq:
        if len(digit) == len(SEGMENTS[0]):
            known[0] = digit
        elif len(digit) == len(SEGMENTS[2]):
            if known[1].issubset(digit):
                known[3] = digit
            else:
                known[2] = digit
    return known


def outputs(line):
    uniq, output = line
    digits = [k for o in output for k, v in isolate(uniq).items() if set(v) == o]
    return sum(place * 10 ** i for i, place in enumerate(reversed(digits)))


def matches(lines, num):
    return sum(len(out) == len(SEGMENTS[num]) for line in lines for out in line[1])


with open("day08.txt") as fin:
    ins = list(parse(fin))

res1 = sum(matches(ins, num) for num in (1, 4, 7, 8))
print(f"Result 1: {res1}")
res2 = sum(outputs(line) for line in ins)
print(f"Result 2: {res2}")
