import itertools

from aocd import get_data, submit

DAY = 11
YEAR = 2023


def part(data: str, expansion: int) -> str:
    grid = data.splitlines()
    stars = []
    n, m = len(grid), len(grid[0])
    rows = set(range(n))
    cols = set(range(m))
    for i in range(n):
        for j in range(m):
            if grid[i][j] == "#":
                if i in rows:
                    rows.remove(i)
                if j in cols:
                    cols.remove(j)
                stars.append((i, j))
    res = 0
    for (y1, x1), (y2, x2) in itertools.combinations(stars, 2):
        dy = abs(y1 - y2)
        dx = abs(x2 - x1)
        dist = dx + dy
        for row in rows:
            if min(y1, y2) < row < max(y1, y2):
                dist += expansion
        for col in cols:
            if min(x1, x2) < col < max(x1, x2):
                dist += expansion
        res += dist
    return str(res)


if __name__ == '__main__':
    input_data = get_data(day=DAY, year=YEAR)
    ans1 = part(input_data, 1)
    print(ans1)
    # submit(answer=ans1, day=DAY, year=YEAR, part=1)
    ans2 = part(input_data, 999999)
    print(ans2)
    # submit(answer=ans2, day=DAY, year=YEAR, part=2)
