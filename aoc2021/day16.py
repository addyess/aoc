from __future__ import annotations
from typing import Union, Generator
from dataclasses import dataclass
import math


class Bitstream:
    def __init__(self, stream):
        self.stream = stream
        self.nib, self.bit = 0, 8

    @property
    def current(self):
        return int(self.stream[self.nib], 16) if self else 0

    def take(self, n, val=0):
        for _ in range(n):
            val = (val << 1) + bool(self.current & self.bit)
            self.bit = 8 if self.bit == 1 else self.bit >> 1
            self.nib = self.nib + 1 if self.bit == 8 else self.nib
        return val

    def __bool__(self):
        return self.nib < len(self.stream)


@dataclass
class Packet:
    ver: int
    typ: int
    length: int
    _val: int
    subs: list[Packet]

    def __len__(self):
        return self.length

    @property
    def val(self):
        return self._val

    @classmethod
    def literal(cls, ver, typ, bitstream):
        taken, val, more = 6, 0, True
        while more:
            nib, taken = bitstream.take(5), taken + 5
            more, val = nib & 0x10, (val << 4) + (nib & 0xF)
        return cls(ver, typ, taken, val, [])


@dataclass
class Operator(Packet):
    def __init__(self, ver, typ, bitstream):
        if bitstream.take(1):
            sub_count = bitstream.take(11)
            sub_stream = mk_packets(bitstream)
            subs = [next(sub_stream) for _ in range(sub_count)]
            taken = 18 + sum(map(len, subs))
        else:
            tot = bitstream.take(15)
            subs, sub_stream = [], mk_packets(bitstream)
            while sum(map(len, subs)) < tot:
                subs.append(next(sub_stream))
            taken = 22 + tot
        super(Operator, self).__init__(ver, typ, taken, None, subs)

    @property
    def val(self):
        if self.typ == 0:
            return sum(_.val for _ in self.subs)
        elif self.typ == 1:
            return math.prod(_.val for _ in self.subs)
        elif self.typ == 2:
            return min(_.val for _ in self.subs)
        elif self.typ == 3:
            return max(_.val for _ in self.subs)
        elif self.typ == 5:
            left, right = self.subs
            return left.val > right.val
        elif self.typ == 6:
            left, right = self.subs
            return left.val < right.val
        elif self.typ == 7:
            left, right = self.subs
            return left.val == right.val


def mk_packets(stream: Union[str, Bitstream]) -> Generator[Packet]:
    if isinstance(stream, str):
        stream = Bitstream(stream.strip())
    while stream:
        ver = stream.take(3)
        typ = stream.take(3)
        if not stream:
            return
        if typ == 4:
            yield Packet.literal(ver, typ, stream)
        else:
            yield Operator(ver, typ, stream)


def sum_versions(l_packets):
    return sum(pkt.ver + sum_versions(pkt.subs) for pkt in l_packets)


with open("day16.txt") as fin:
    packets = list(mk_packets(fin.read()))
print(f"Result #1: {sum_versions(packets)}")
print(f"Result #2: {sum(_.val for _ in packets)}")
