#! /usr/bin/python3
from aoc.file import puzzle_input

PKT_EXAMPLES = [
    ("bvwbjplbgvbhsrlpgdmjqwftvncz", 5),
    ("nppdvjthqldpwncqszvftbrmjlhg", 6),
    ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10),
    ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11),
]

MSG_EXAMPLES = [
    ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 19),
    ("bvwbjplbgvbhsrlpgdmjqwftvncz", 23),
    ("nppdvjthqldpwncqszvftbrmjlhg", 23),
    ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 29),
    ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 26),
]


def start_of_(key_len, seq):
    window, seq = seq[: key_len - 1], seq[key_len - 1 :]
    for pos, char in enumerate(seq):
        window += char
        if len(set(window)) == key_len:
            return pos + key_len
        window = window[1:]


for sequence, num in PKT_EXAMPLES:
    assert start_of_(4, sequence) == num

for sequence, num in MSG_EXAMPLES:
    assert start_of_(14, sequence) == num

elf_stream = next(puzzle_input())
res1 = start_of_(4, elf_stream)
print(f"Result 1: {res1}")
res2 = start_of_(14, elf_stream)
print(f"Result 2: {res2}")
