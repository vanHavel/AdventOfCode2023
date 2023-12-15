import re

from aocd import get_data, submit

DAY = 15
YEAR = 2023


def h(s: str) -> int:
    acc = 0
    for c in s:
        acc += ord(c)
        acc *= 17
        acc %= 256
    return acc


def part1(data: str) -> str:
    words = data.split(",")
    res = sum(h(word) for word in words)
    return str(res)


def part2(data: str) -> str:
    words = data.split(",")
    map = {i: {} for i in range(256)}
    for word in words:
        label = re.search(r"[a-z]+", word).group()
        hashed = h(label)
        symbol = re.search(r"[-=]", word).group()
        if symbol == "-" and label in map[hashed]:
            map[hashed].pop(label)
        elif symbol == "=":
            value = re.search(r"\d+", word).group()
            map[hashed][label] = int(value)
    ans = 0
    for i in range(256):
        for index, value in enumerate(map[i].values(), 1):
            ans += (i + 1) * index * value
    return str(ans)



if __name__ == '__main__':
    input_data = get_data(day=DAY, year=YEAR)
    test_data = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""
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
