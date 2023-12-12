import copy
import functools
import re

from aocd import get_data, submit

DAY = 12
YEAR = 2023

way = []
target = []

def part1(data: str) -> str:
    lines = data.splitlines()
    res = 0
    for line in lines:
        way, target = line.split(" ")
        way = [c for c in way]
        target = [int(x) for x in target.split(",")]
        strs = backtrack(way, 0, 0)
        res += sum([l == target for l in strs])
    return str(res)


def backtrack(line, pos, ip) -> list[list[int]]:
    if pos == len(line):
        return [[ip]] if ip else [[]]
    if line[pos] == "." and ip > 0:
        return [[ip] + rec for rec in backtrack(line, pos+1, 0)]
    if line[pos] == "." and ip == 0:
        return backtrack(line, pos+1, 0)
    if line[pos] == "#":
        return backtrack(line, pos+1, ip+1)
    if line[pos] == "?":
        line[pos] = "."
        a1 = backtrack(line, pos, ip)
        line[pos] = "#"
        a2 = backtrack(line, pos, ip)
        line[pos] = "?"
        return a1 + a2


def part2(data: str) -> str:
    lines = data.splitlines()
    res = 0
    for line in lines:
        w, ts = line.split(" ")
        w = [c for c in w]
        global way
        way = w + ["?"] + w + ["?"] + w + ["?"] + w + ["?"] + w + [".", "."]
        global target
        target = [int(x) for x in ts.split(",")]
        target *= 5
        count = backtrack2(0, 0, way[0])
        backtrack2.cache_clear()
        res += count
    return str(res)


@functools.lru_cache(maxsize=None)
def backtrack2(pos: int, tpos: int, c: str) -> int:
    global way
    global target
    if pos > len(way):
        return 0
    if pos == len(way):
        return tpos == len(target)
    if way[pos] == ".":
        return backtrack2(pos+1, tpos, way[pos+1] if len(way) > pos+1 else ".")
    if way[pos] == "#":
        if tpos >= len(target):
            return 0
        t = target[tpos]
        prefix = way[pos:pos+t]
        if pos + t > len(way):
            return 0
        if not all([c != "." for c in prefix]):
            return 0
        if way[pos+t] == "#":
            return 0
        rec = backtrack2(pos + t + 1, tpos + 1, way[pos+t+1])
        return rec
    if way[pos] == "?":
        way[pos] = "."
        s1 = backtrack2(pos, tpos, ".")
        way[pos] = "#"
        s2 = backtrack2(pos, tpos, "#")
        way[pos] = "?"
        return s1 + s2


if __name__ == '__main__':
    input_data = get_data(day=DAY, year=YEAR)
    ans1 = part1(input_data)
    print(ans1)
    # submit(answer=ans1, day=DAY, year=YEAR, part=1)
    ans2 = part2(input_data)
    print(ans2)
    # submit(answer=ans2, day=DAY, year=YEAR, part=2)
