import sys

from aocd import get_data, submit

DAY = 1
YEAR = 2023


def part1(data: str) -> str:
    lines = data.splitlines()
    return str(lines)


def part2(data: str) -> str:
    lines = data.splitlines()
    return str(lines)


if __name__ == '__main__':
    sys.setrecursionlimit(1_000_000)
    input_data = get_data(day=DAY, year=YEAR)
    test_data = r""""""
    test1 = part1(test_data)
    ans1 = part1(input_data)
    print(test1)
    print(ans1)
    # submit(answer=ans1, day=DAY, year=YEAR, part=1)
    test2 = part2(test_data)
    ans2 = part2(input_data)
    print(test2)
    print(ans2)
    # submit(answer=ans2, day=DAY, year=YEAR, part=2)
