import itertools
import re
from math import lcm

from aocd import get_data, submit

DAY = 8
YEAR = 2023


def part1(data: str) -> str:
    lines = data.splitlines()
    route, rules = lines[0], lines[2:]
    nav = {}
    for rule in rules:
        start, left, right = re.findall(r"[A-Z][A-Z][A-Z]", rule)
        nav[start] = {"L": left, "R": right}
    pos = "AAA"
    steps = 0
    for cmd in itertools.cycle(route):
        pos = nav[pos][cmd]
        steps += 1
        if pos == "ZZZ":
            return str(steps)


def part2(data: str) -> str:
    lines = data.splitlines()
    route, rules = lines[0], lines[2:]
    nav = {}
    for rule in rules:
        start, left, right = re.findall(r"[A-Z0-9][A-Z0-9][A-Z0-9]", rule)
        nav[start] = {"L": left, "R": right}
    poss = [pos for pos in nav if pos.endswith("A")]
    loops = []
    for pos in poss:
        steps = 0
        for cmd in itertools.cycle(route):
            pos = nav[pos][cmd]
            steps += 1
            if pos.endswith("Z"):
                loops.append(steps)
                break
    return str(lcm(*loops))


if __name__ == '__main__':
    input_data = get_data(day=DAY, year=YEAR)
    ans1 = part1(input_data)
    print(ans1)
    # submit(answer=ans1, day=DAY, year=YEAR, part=1)
    ans2 = part2(input_data)
    print(ans2)
    # submit(answer=ans2, day=DAY, year=YEAR, part=2)
