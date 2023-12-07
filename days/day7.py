import re
from collections import Counter
from functools import cmp_to_key

from aocd import get_data, submit

DAY = 7
YEAR = 2023


def part(data: str, part: int) -> str:
    lines = data.splitlines()
    hands, bids = [], []
    for line in lines:
        hand, bid = line.split()
        hands.append(hand)
        bids.append(int(bid))
    zipped = zip(hands, bids)
    sortzip = sorted(zipped, key=cmp_to_key(lambda t1, t2: compare(t1, t2, part)))
    res = 0
    for index, (hand, bid) in enumerate(sortzip, 1):
        res += bid * index
    return str(res)


def compare(t1: tuple[str, int], t2: tuple[str, int], part: int) -> int:
    hand1 = t1[0]
    hand2 = t2[0]
    if score(hand1, part) < score(hand2, part):
        return -1
    elif score(hand1, part) > score(hand2, part):
        return 1
    else:
        for d1, d2 in zip(hand1, hand2):
            v1 = value_map(d1, part)
            v2 = value_map(d2, part)
            if v1 < v2:
                return -1
            if v1 > v2:
                return 1


def value_map(d: str, part: int) -> int:
    if d.isdigit():
        return int(d)
    elif d == "T":
        return 10
    elif d == "J":
        if part == 1:
            return 11
        else:
            return 1
    elif d == "Q":
        return 12
    elif d == "K":
        return 13
    elif d == "A":
        return 14
    else:
        print(d)
        raise ValueError


def score(hand: str, part: int) -> int:
    counts = Counter(sorted(hand))
    values = sorted(list(counts.values()))
    if part == 2:
        jokers = counts.get("J")
        others = {key: value for key, value in counts.items() if key != "J"}
        rest = "".join([c for c in hand if c != "J"])
        suits = ["A", "K", "Q", "T"] + [str(i) for i in range(2,10)]
        if jokers == 5:
            return 10
        elif jokers == 4:
            return 10
        elif jokers == 3:
            if list(others.values()) == [1, 1]:
                return 9
            elif list(others.values()) == [2]:
                return 10
        elif jokers == 2:
            return max([score(rest + c1 + c2, 1) for c1 in suits for c2 in suits])
        elif jokers == 1:
            return max([score(rest + c, 1) for c in suits])

    if values == [5]:
        return 10
    elif values == [1, 4]:
        return 9
    elif values == [2, 3]:
        return 8
    elif values == [1, 1, 3]:
        return 7
    elif values == [1, 2, 2]:
        return 6
    elif values == [1, 1, 1, 2]:
        return 5
    return 4


if __name__ == '__main__':
    input_data = get_data(day=DAY, year=YEAR)
    ans1 = part(input_data, 1)
    print(ans1)
    #submit(answer=ans1, day=DAY, year=YEAR, part=1)
    ans2 = part(input_data, 2)
    print(ans2)
    #submit(answer=ans2, day=DAY, year=YEAR, part=2)
