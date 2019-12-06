ins = range(367479, 893698)


def has_double(pwd):
    for _ in range(5):
        l, r = pwd[_:_+2]
        if l == r:
            return True
    return False


def has_at_least_one_double(pwd):
    p = ''
    for _ in range(5):
        (l, r), tail = pwd[_:_+2], pwd[_+2:_+3]
        if p != l == r and tail != l:
            return True
        p = l
    return False


def increasing(pwd):
    for _ in range(5):
        l, r = pwd[_:_+2]
        if l > r:
            return False
    return True


possible = [_ for _ in ins if has_double(str(_)) and increasing(str(_))]
print(f"Result 1: {len(possible)}")

assert has_at_least_one_double("111122")

possible = [_ for _ in ins if has_at_least_one_double(str(_)) and increasing(str(_))]
print(f"Result 2: {len(possible)}")
