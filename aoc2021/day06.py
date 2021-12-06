#! /usr/bin/python3
class LanternFish:
    @classmethod
    def parse(cls, line):
        return cls([int(_) for _ in line.split(",")])

    def __init__(self, initial):
        self.current = {age: initial.count(age) for age in range(9)}

    def age(self):
        producers = self.current.pop(0, 0)
        self.current = {(age - 1): count for age, count in self.current.items()}
        self.current[6] += producers
        self.current[8] = producers

    @property
    def total(self):
        return sum(self.current.values())


with open("day06.txt") as fin:
    ins = fin.read()
school = LanternFish.parse(ins)
for _ in range(80):  # After 80 days
    school.age()
print(f"Result 1: {school.total}")
for _ in range(256 - 80):  # After 256 days
    school.age()
print(f"Result 2: {school.total}")
