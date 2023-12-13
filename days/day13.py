import copy

from aocd import get_data, submit

DAY = 13
YEAR = 2023


def part1(data: str) -> str:
    grids = data.split("\n\n")
    ans = 0
    for sgrid in grids:
        grid = sgrid.splitlines()
        for t in find(grid):
            factor = 1 if t[1] == "v" else 100
            ans += factor * t[0]

    return str(ans)


def part2(data: str) -> str:
    grids = data.split("\n\n")
    ans = 0
    for sgrid in grids:
        grid = sgrid.splitlines()
        normal = [c for c in find(grid)][0]
        n = len(grid)
        m = len(grid[0])
        for si in range(n):
            for sj in range(m):
                sgrid = copy.deepcopy(grid)
                if sgrid[si][sj] == ".":
                    sgrid[si] = sgrid[si][:sj] + "#" + sgrid[si][sj+1:]
                else:
                    sgrid[si] = sgrid[si][:sj] + "." + sgrid[si][sj + 1:]
                for t in find(sgrid):
                    if t != normal:
                        factor = 1 if t[1] == "v" else 100
                        ans += factor * t[0]
    return str(ans // 2)


def find(grid):
    n = len(grid)
    m = len(grid[0])
    # cols
    for i in range(1, m):
        ok = True
        for j in range(m):
            if i - j - 1 < 0:
                continue
            if i + j >= m:
                continue
            for k in range(n):
                if grid[k][i - j - 1] != grid[k][i + j]:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            yield (i, "v")
    # rows
    for i in range(1, n):
        ok = True
        for j in range(n):
            if i - j - 1 < 0:
                continue
            if i + j >= n:
                continue
            for k in range(m):
                if grid[i + j][k] != grid[i - j - 1][k]:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            yield (i, "h")


if __name__ == '__main__':
    input_data = get_data(day=DAY, year=YEAR)
    test_data = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""
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
