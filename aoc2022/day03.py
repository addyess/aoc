#! /usr/bin/python3
from aoc.file import example, puzzle_input


def find_compartment_match(line):
    c1, c2 = map(set, (line[: len(line) // 2], line[len(line) // 2 :]))
    return (c1 & c2).pop()


def find_group_id(group):
    e1, e2, e3 = map(set, group)
    return (e1 & e2 & e3).pop()


def priority(match):
    base, adder = ("a", 1) if "a" <= match <= "z" else ("A", 27)
    return ord(match) - ord(base) + adder


def solver(lines):
    rucksack_total, badge_total = 0, 0
    groups = []
    for line_no, line in enumerate(lines):
        rucksack_total += priority(find_compartment_match(line))
        if line_no % 3 == 0:
            groups.append([])
        groups[-1].append(line)

    for group in groups:
        badge_total += priority(find_group_id(group))
    return rucksack_total, badge_total


rucksack_total, badge_total = solver(
    example(
        """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""
    )
)
assert rucksack_total == 157
assert badge_total == 70

rucksack_total, badge_total = solver(puzzle_input())
print(f"Result 1 {rucksack_total}")
print(f"Result 2 {badge_total}")
