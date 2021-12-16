with open("day9.txt") as fin:
    ins = fin.read()


def groups(text, score=0):
    garb = 0
    garb_counted, accum = 0, 0
    try:
        while True:
            head, tail = next(text), text
            if head == "!":
                next(text), text
            elif head == "<" and not garb:
                garb += 1
            elif head == ">" and garb:
                garb_counted += garb - 1
                garb = 0
            elif head == "{" and not garb:
                inner = groups(tail, score=score + 1)
                accum += inner[0]
                garb_counted += inner[1]
            elif head == "}" and not garb:
                return score + accum, garb_counted
            elif garb:
                garb += 1
    except StopIteration:
        return accum + score, garb_counted


# assert groups(iter('{}')) == 1
# assert groups(iter('{{{}}}')) == 6
# assert groups(iter('{{}{}}')) == 5
# assert groups(iter('{{{},{},{{}}}}')) == 16
# assert groups(iter('{<a>,<a>,<a>,<a>}')) == 1
# assert groups(iter('{{<ab>},{<ab>},{<ab>},{<ab>}}')) == 9
# assert groups(iter('{{<!!>},{<!!>},{<!!>},{<!!>}}')) == 9
# assert groups(iter('{{<a!>},{<a!>},{<a!>},{<ab>}}')) == (3, 0)
assert groups(iter("<>")) == (0, 0)
assert groups(iter("<random characters>")) == (0, 17)
assert groups(iter("<<<<>")) == (0, 3)
assert groups(iter("<{!>}>")) == (0, 2)
assert groups(iter("<!!>")) == (0, 0)
assert groups(iter("<!!!>>")) == (0, 0)
assert groups(iter('<{o"i!a,<{i<a>')) == (0, 10)
print(f"Result 1: {groups(iter(ins))}")
