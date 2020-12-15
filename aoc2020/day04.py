import re
from utils import GroupParsed
from functools import partial

with open("day04.txt") as f_in:
    ins = [_.strip() for _ in f_in]


class License(GroupParsed):
    def __init__(self, data):
        line = " ".join(data).split()
        self._ = dict(_.split(":") for _ in line)

    def meets_reqs(self):
        return set('byr iyr eyr hgt hcl ecl pid'.split()).issubset(self._.keys())

    def valid_4_digit(self, num):
        num = self._[num]
        return int(num) if re.match(r"^\d{4}$", num) else -1

    def valid_height(self):
        search = re.search(r"^(\d+)(cm|in)$", self._['hgt'])
        if search:
            value, units = search.groups()
            if units == "cm":
                return 150 <= int(value) <= 193
            return 59 <= int(value) <= 76
        return False

    valid_hcl = partial(re.compile(r'^#[0-9a-f]{6}$').match)
    valid_pid = partial(re.compile(r"^\d{9}$").match)
    valid_eye = partial(re.compile(r"^(amb|blu|brn|gry|grn|hzl|oth)$").match)

    def strict_req(self):
        return all([
            1920 <= self.valid_4_digit('byr') <= 2002,
            2010 <= self.valid_4_digit('iyr') <= 2020,
            2020 <= self.valid_4_digit('eyr') <= 2030,
            self.valid_height(),
            self.valid_hcl(self._['hcl']),
            self.valid_eye(self._['ecl']),
            self.valid_pid(self._['pid'])
        ])


records = list(License.parsed(ins))
res1 = [_ for _ in records if _.meets_reqs()]
print(f"Result 1: {len(res1)}")
res2 = [_ for _ in res1 if _.strict_req()]
print(f"Result 2: {len(res2)}")