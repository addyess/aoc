import re
import functools

with open("day04.txt") as f_in:
    ins = [_.strip() for _ in f_in.readlines()]


class Record:
    @classmethod
    def parsed(cls, data):
        record = {}
        for line in data:
            if not line:
                yield cls(record)
                record = {}
            else:
                record.update(dict(pair.split(":") for pair in line.split()))
        yield cls(record)

    def __init__(self, data):
        self._ = data

    def meets_reqs(self):
        return set('byr iyr eyr hgt hcl ecl pid'.split()).issubset(self._.keys())

    def valid_4_digit(self, num):
        num = self._[num]
        return int(num) if re.match(r"^\d{4}$", num) else -1

    def valid_height(self):
        search = re.search(r"^(\d+)(cm|in)$", self._['hgt'])
        if not search:
            return False
        value, units = search.groups()
        if units == "cm":
            return 150 <= int(value) <= 193
        return 59 <= int(value) <= 76

    valid_hair = functools.partial(re.match, r'^#[0-9a-f]{6}$')
    valid_pid = functools.partial(re.match,  r"^\d{9}$")
    valid_eye = functools.partial(re.match,  r"^(amb|blu|brn|gry|grn|hzl|oth)$")

    def strict_req(self):
        return all([
            1920 <= self.valid_4_digit('byr') <= 2002,
            2010 <= self.valid_4_digit('iyr') <= 2020,
            2020 <= self.valid_4_digit('eyr') <= 2030,
            self.valid_height(),
            self.valid_hair(self._['hcl']),
            self.valid_eye(self._['ecl']),
            self.valid_pid(self._['pid'])
        ])


records = list(Record.parsed(ins))
res1 = [_ for _ in records if _.meets_reqs()]
print(f"Result 1: {len(res1)}")
res2 = [_ for _ in res1 if _.strict_req()]
print(f"Result 2: {len(res2)}")