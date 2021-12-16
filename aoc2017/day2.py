with open("day2.txt") as fin:
    lines = [[int(i) for i in _.strip().split("\t")] for _ in fin.readlines()]


def cksum(row):
    return max(row) - min(row)


def even_div(row):
    while row:
        head, row = row[0], row[1:]
        for tail in row:
            if head % tail == 0:
                return head // tail
            if tail % head == 0:
                return tail // head


res1 = sum(cksum(row) for row in lines)
print(f"Result 1: {res1}")

res2 = sum(even_div(row) for row in lines)
print(f"Result 2: {res2}")
