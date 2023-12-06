import re

from aocd import get_data, submit

DAY = 6
YEAR = 2023


def part1(data: str) -> str:
    times, distances = data.splitlines()
    times = [int(x) for x in times.split(":")[1].split()]
    distances = [int(x) for x in distances.split(":")[1].split()]
    res = 1
    for time, distance in zip(times, distances):
        ways = 0
        for i in range(1, time):
            speed = i
            dist = (time - i) * speed
            if dist > distance:
                ways += 1
        print(ways)
        res *= ways
    return str(res)


def part2(data: str) -> str:
    times, distances = data.splitlines()
    time = int("".join([x for x in times.split(":")[1].split()]))
    distance = int("".join([x for x in distances.split(":")[1].split()]))
    print(time, distance)
    ways = 0
    for i in range(1, time):
        speed = i
        dist = (time - i) * speed
        if dist > distance:
            ways += 1
    print(ways)
    return str(ways)


if __name__ == '__main__':
    input_data = get_data(day=DAY, year=YEAR)
    ans1 = part1(input_data)
    print(ans1)
    #submit(answer=ans1, day=DAY, year=YEAR, part=1)
    ans2 = part2(input_data)
    print(ans2)
    submit(answer=ans2, day=DAY, year=YEAR, part=2)
