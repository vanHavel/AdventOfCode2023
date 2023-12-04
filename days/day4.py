import re

from aocd import get_data, submit

DAY = 4
YEAR = 2023


def intersect_line(line: str) -> int:
    prefix, content = line.split(":")
    left, right = content.split("|")
    left_set = {int(x) for x in left.strip().split()}
    right_set = {int(x) for x in right.strip().split()}
    intersection = left_set & right_set
    return len(intersection)

def part1(data: str) -> str:
    score = 0
    for line in data.splitlines():
        intersection = intersect_line(line)
        score += int(2 ** (intersection - 1))
    return str(score)


def part2(data: str) -> str:
    lines = data.splitlines()
    counts = [1] * len(lines)
    for i in range(len(lines)):
        line = lines[i]
        intersection = intersect_line(line)
        for j in range(i + 1, i + 1 + intersection):
            counts[j] += counts[i]
    return str(sum(counts))


if __name__ == '__main__':
    input_data = get_data(day=DAY, year=YEAR)
    ans1 = part1(input_data)
    print(ans1)
    # submit(answer=ans1, day=DAY, year=YEAR, part=1)
    ans2 = part2(input_data)
    print(ans2)
    submit(answer=ans2, day=DAY, year=YEAR, part=2)
