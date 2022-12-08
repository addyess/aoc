#! /usr/bin/python3
from aoc.file import puzzle_input, example
import re

EX_TEXT = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

CD_CMD = re.compile(r"^\$ cd (?P<dir>\S+)")
FILE_LS = re.compile(r"^(?P<size>\d+) (?P<file>\S+)")
FS_SZ = 70000000
UPDATE_SZ = 30000000


def parse_fs(lines):
    fs = {".": 0}
    for line in lines:
        if m := CD_CMD.match(line):
            dir = m.group("dir")
            if dir == "..":
                return fs
            fs[dir] = parse_fs(lines)
            fs["."] += fs[dir]["."]
        elif m := FILE_LS.match(line):
            sz = int(m.group("size"))
            fs[m.group("file")] = sz
            fs["."] += sz
    return fs


def dir_sizes(fs):
    sizes = [fs["."]]
    for path in fs.values():
        if isinstance(path, dict):
            sizes.extend(dir_sizes(path))
    return sizes


def solver(lines):
    fs = parse_fs(lines)
    dir_sz = dir_sizes(fs)
    total = sum(_ for _ in dir_sz if _ <= 100000)
    delete_sz = UPDATE_SZ - FS_SZ + fs["/"]["."]
    sacrifice_sz = sorted(_ for _ in dir_sz if _ >= delete_sz)[0]
    return total, sacrifice_sz


res1, res2 = solver(example(EX_TEXT))
assert (res1, res2) == (95437, 24933642)
res1, res2 = solver(puzzle_input())
print(f"Result 1: {res1}")
print(f"Result 2: {res2}")
