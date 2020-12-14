from math import prod
from urllib.parse import urlencode

with open("day13.txt") as f_in:
    ins = [_.strip() for _ in f_in]


class Bus:
    @classmethod
    def parse(cls, bus_list):
        return [
            (t, cls(_id)) for t, _id in enumerate(bus_list.split(","))
            if _id != "x"
        ]

    def __init__(self, bus_id):
        self.id = int(bus_id)

    def next_departure(self, after):
        return self.id - after % self.id


def wolfram_alpha(busses):
    """Build Query for Chinese Remainder Theory."""
    return ",".join(f"(n+{i})%{bus.id} = 0" for i, bus in busses)


my_arrival = int(ins[0])
busses = Bus.parse(ins[1])
next_bus = min(
    (bus.next_departure(my_arrival), bus.id)
    for _, bus in busses
)
print(f"Result 1: {prod(next_bus)}")
query = urlencode({'i': wolfram_alpha(busses)})
print(f"Result 2: https://www.wolframalpha.com/input/?" + query)
print("Click the link -- take the integer part of n = <to-discard>m + <to-keep>")
