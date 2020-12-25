from itertools import count

PRIME = 20201227

with open("day25.txt") as f_in:
    card_pub, door_pub = [int(_.strip()) for _ in f_in]


def trial_and_error(p1, p2):
    value, subject_number = 1, 7
    for loop_size in count(0):
        value *= subject_number
        value %= PRIME
        if value == p1:
            return p2, loop_size + 1
        if value == p2:
            return p1, loop_size + 1


pub_key, loop = trial_and_error(card_pub, door_pub)
print(f"Result 1: {pow(pub_key, loop, PRIME)}")
