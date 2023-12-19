import sys

from aocd import get_data, submit

from util.grid import *

DAY = 18
YEAR = 2023


def part1(data: str) -> str:
    size = 400
    lines = data.splitlines()
    grid = Grid((False for i in range(size)) for j in range(size))
    pos = (300, 110)
    grid.set(pos, True)
    for line in lines:
        dir, length, code = line.split()
        dir = parse_dir(dir)
        length = int(length)
        for i in range(length):
            pos = move(pos, dir)
            grid.set(pos, True)
    floodfill(grid, (0, 0))
    count = 0
    for pos in grid.positions():
        if not grid.meta(pos, "out"):
            count += 1
    return str(count)


def floodfill(grid: Grid, pos: Pos) -> None:
    if grid.meta(pos, "out") or grid.get(pos):
        return
    grid.mark(pos, "out", True)
    for dir in Dir:
        next = move(pos, dir)
        if grid.inside(next):
            floodfill(grid, next)


def parse_dir(s: str) -> Dir:
    if s == "U":
        return Dir.N
    elif s == "R":
        return Dir.E
    elif s == "D":
        return Dir.S
    elif s == "L":
        return Dir.W
    else:
        raise ValueError


def part2(data: str) -> str:
    commands = data.splitlines()
    pos = (0, 0)
    lines = []
    for command in commands:
        d, l, code = command.split()
        length = int(code[2:7], 16)
        dir = [Dir.E, Dir.S, Dir.W, Dir.N][int(code[7])]
        next = move(pos, dir, length)
        if dir in [Dir.N, Dir.S]:
            x, y1, y2 = pos[1], pos[0], next[0]
            lines.append((x, min(y1, y2), max(y1, y2)))
        pos = next
    lines = sorted(lines)
    ans = 0
    prevx = None
    open = []
    for (x, y1, y2) in lines:
        if prevx is not None and prevx < x:
            for o in open:
                print("fill", prevx, x, o)
                ans += (o[1] - o[0] + 1) * (x - prevx)
        prevx = x
        endsy1 = [o for o in open if o[1] == y1]
        endsy2 = [o for o in open if o[1] == y2]
        startsy1 = [o for o in open if o[0] == y1]
        startsy2 = [o for o in open if o[0] == y2]
        contains = [o for o in open if o[0] < y1 < y2 < o[1]]
        if (y1, y2) in open:
            open.remove((y1, y2))
            print("kill", (y1, y2))
            ans += y2 - y1 + 1
        elif endsy1 and startsy2:
            endsy1, startsy2 = endsy1[0], startsy2[0]
            print("join", (endsy1[0], startsy2[1]))
            open.remove(endsy1)
            open.remove(startsy2)
            open.append((endsy1[0], startsy2[1]))
        elif startsy2:
            startsy2 = startsy2[0]
            print("extend D", (y1, startsy2[1]))
            open.remove(startsy2)
            open.append((y1, startsy2[1]))
        elif endsy1:
            endsy1 = endsy1[0]
            print("extend U", (endsy1[0], y2))
            open.remove(endsy1)
            open.append((endsy1[0], y2))
        elif endsy2:
            endsy2 = endsy2[0]
            print("shrink D", (endsy2[0], y1))
            open.remove(endsy2)
            open.append((endsy2[0], y1))
            ans += y2 - y1
        elif startsy1:
            startsy1 = startsy1[0]
            print("shrink U", (y2, startsy1[1]))
            open.remove(startsy1)
            open.append((y2, startsy1[1]))
            ans += y2 - y1
        elif contains:
            contains = contains[0]
            print("split", (contains[0], y1), (y2, contains[1]))
            open.remove(contains)
            open.append((contains[0], y1))
            open.append((y2, contains[1]))
            ans += y2 - y1 - 1
        else:
            print("add", (y1, y2))
            open.append((y1, y2))
    return str(ans)


if __name__ == '__main__':
    sys.setrecursionlimit(1_000_000)
    input_data = get_data(day=DAY, year=YEAR)
    ans1 = part1(input_data)
    print(ans1)
    # submit(answer=ans1, day=DAY, year=YEAR, part=1)
    ans2 = part2(input_data)
    print(ans2)
    # submit(answer=ans2, day=DAY, year=YEAR, part=2)
