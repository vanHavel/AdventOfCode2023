import sys

from aocd import get_data, submit

DAY = 24
YEAR = 2023


def part1(data: str, minc: int, maxc: int) -> str:
    lines = data.splitlines()
    starts = []
    speeds = []
    for line in lines:
        start, speed = line.split("@")
        start = tuple(map(int, start.split(",")))
        speed = tuple(map(int, speed.split(",")))
        starts.append(start)
        speeds.append(speed)
    zipped = list(zip(starts, speeds))
    ans = 0
    for i in range(len(zipped)):
        for j in range(i + 1, len(zipped)):
            x1, y1, _ = zipped[i][0]
            x2, y2, _ = zipped[j][0]
            vx1, vy1, _ = zipped[i][1]
            vx2, vy2, _ = zipped[j][1]
            # same start
            if x1 == x2 and y1 == y2:
                if minc <= x1 <= maxc and minc <= y1 <= maxc:
                    ans += 1
                continue
            # parallel
            if vx1 * vy2 == vx2 * vy1:
                continue
            # intersection
            # x1 + vx1 * t1 = x2 + vx2 * t2
            # y1 + vy1 * t1 = y2 + vy2 * t2
            t1 = ((x2 - x1) * vy2 + (y1 - y2) * vx2) / (vx1 * vy2 - vx2 * vy1)
            t2 = ((x2 - x1) * vy1 + (y1 - y2) * vx1) / (vx1 * vy2 - vx2 * vy1)
            sx = x1 + vx1 * t1
            sy = y1 + vy1 * t1
            if t1 > 0 and t2 > 0 and minc <= sx <= maxc and minc <= sy <= maxc:
                ans += 1

    return str(ans)


def part2(data: str) -> str:
    lines = data.splitlines()
    starts = []
    speeds = []
    for line in lines:
        start, speed = line.split("@")
        start = tuple(map(int, start.split(",")))
        speed = tuple(map(int, speed.split(",")))
        starts.append(start)
        speeds.append(speed)
    wolfram = "Solve["
    for index, (start, speed) in enumerate(zip(starts, speeds), 1):
        if index > 3:
            break
        x, y, z = start
        v, w, u = speed
        # x + v * t = a + d * t
        # y + w * t = b + e * t
        # z + u * t = c + f * t
        time = chr(ord("t") - index + 1)
        wolfram += f"{x} {v if v < 0 else f'+ {v}'} * {time} == a + d * {time} && "
        wolfram += f"{y} {w if w < 0 else f'+ {w}'} * {time} == b + e * {time} && "
        wolfram += f"{z} {u if u < 0 else f'+ {u}'} * {time} == c + f * {time} && "
    wolfram = wolfram[:-4] + ", {a, b, c, d, e, f, r, s, t}]"
    return wolfram


if __name__ == '__main__':
    sys.setrecursionlimit(1_000_000)
    input_data = get_data(day=DAY, year=YEAR)
    ans1 = part1(input_data, 200000000000000, 400000000000000)
    print(ans1)
    # submit(answer=ans1, day=DAY, year=YEAR, part=1)
    ans2 = part2(input_data)
    print(ans2)
    # submit(answer=ans2, day=DAY, year=YEAR, part=2)
