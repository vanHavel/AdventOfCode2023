import re

from aocd import get_data, submit

DAY = 1
YEAR = 2023


def part1(data: str) -> str:
    lines = data.splitlines()
    digits = [[c for c in l if c.isdigit()] for l in lines]
    linevals = [int(ds[0]) * 10 + int(ds[-1]) for ds in digits]
    return str(sum(linevals))


def part2(data: str) -> str:
    lines = data.splitlines()
    digit_strings = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    regex = f"(?=({'|'.join(digit_strings + [str(i) for i in range(1, 10)])}))"
    res = 0
    for line in lines:
        matches = list(re.finditer(regex, line))
        first_digit = digit_strings.index(matches[0].group(1)) + 1 if matches[0].group(1) in digit_strings else int(matches[0].group(1))
        last_digit = digit_strings.index(matches[-1].group(1)) + 1 if matches[-1].group(1) in digit_strings else int(matches[-1].group(1))
        res += first_digit * 10 + last_digit
    return str(res)


if __name__ == '__main__':
    input_data = get_data(day=DAY, year=YEAR)
    ans1 = part1(input_data)
    print(ans1)
    # submit(answer=ans1, day=DAY, year=YEAR, part=1)
    ans2 = part2(input_data)
    print(ans2)
    # submit(answer=ans1, day=DAY, year=YEAR, part=2)
