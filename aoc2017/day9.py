with open("day9.txt") as fin:
    ins = fin.read()


def groups(text, score=0):
    garb = False
    accum = 0
    try:
        while True:
            head, tail = next(text), text
            if head == "!":
                head, tail = next(text), text
            elif head == '<' and not garb:
                garb = True
            elif head == '>' and garb:
                garb = False
            elif head == '{' and not garb:
                accum += groups(tail, score=score+1)
            elif head == '}' and not garb:
                return score + accum
    except StopIteration:
        return accum + score


# assert groups(iter('{}')) == 1
# assert groups(iter('{{{}}}')) == 6
# assert groups(iter('{{}{}}')) == 5
# assert groups(iter('{{{},{},{{}}}}')) == 16
# assert groups(iter('{<a>,<a>,<a>,<a>}')) == 1
# assert groups(iter('{{<ab>},{<ab>},{<ab>},{<ab>}}')) == 9
# assert groups(iter('{{<!!>},{<!!>},{<!!>},{<!!>}}')) == 9
assert groups(iter('{{<a!>},{<a!>},{<a!>},{<ab>}}')) == 3
print(f"Result 1: {groups(iter(ins))}")
