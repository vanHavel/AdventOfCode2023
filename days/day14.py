import copy

from aocd import get_data, submit

DAY = 14
YEAR = 2023


def part1(data: str) -> str:
    grid = [[x for x in row] for row in data.splitlines()]
    n, m = len(grid), len(grid[0])
    ngrid = turn(grid, "N")
    score = get_score(ngrid)

    return str(score)


def turn(grid, d):
    grid = copy.deepcopy(grid)
    n, m = len(grid), len(grid[0])
    change = True
    while change:
        change = False
        for i in range(n):
            for j in range(m):
                if grid[i][j] == "O":
                    nxt = move(i, j, d)
                    if valid(grid, nxt):
                        y, x = nxt
                        grid[y][x] = "O"
                        grid[i][j] = "."
                        change = True
    return grid


def move(i, j, d):
    if d == "N":
        return i - 1, j
    elif d == "E":
        return i, j + 1
    elif d == "S":
        return i + 1, j
    elif d == "W":
        return i, j - 1

def valid(grid, pos):
    y, x = pos
    n, m = len(grid), len(grid[0])
    if y >= 0 and x >= 0 and y < n and x < m and grid[y][x] == ".":
        return True
    return False


def part2(data: str) -> str:
    grid = [[x for x in row] for row in data.splitlines()]
    n, m = len(grid), len(grid[0])
    succmap = dict()
    d = "N"
    i = 0
    skipped = False
    while True:
        ngrid, seen = succmap.get((h(grid), d), (None, None))
        if not ngrid:
            ngrid = turn(grid, d)
            succmap[(h(grid), d)] = (copy.deepcopy(ngrid), i)
            grid = ngrid
            d = rotate(d)
            i += 1
        elif not skipped:
            print(i, seen)
            diff = i - seen
            todo = 4_000_000_000 - i
            loops = todo // diff
            print(loops, diff)
            i += loops * diff
            print(i)
            skipped = True
        else:
            grid = ngrid
            d = rotate(d)
            i += 1

        if i == 4_000_000_000:
            break

    score = get_score(grid)

    return str(score)


def h(grid):
    return "".join(["".join(row) for row in grid])


def rotate(d):
    if d == "N":
        return "W"
    elif d == "E":
        return "N"
    elif d == "S":
        return "E"
    elif d == "W":
        return "S"
    raise ValueError


def get_score(grid):
    score = 0
    n, m = len(grid), len(grid[0])
    for i in range(n):
        for j in range(m):
            if grid[i][j] == "O":
                score += (n - i)
    return score


if __name__ == '__main__':
    input_data = get_data(day=DAY, year=YEAR)
    ans1 = part1(input_data)
    print(ans1)
    # submit(answer=ans1, day=DAY, year=YEAR, part=1)
    ans2 = part2(input_data)
    print(ans2)
    # submit(answer=ans2, day=DAY, year=YEAR, part=2)
