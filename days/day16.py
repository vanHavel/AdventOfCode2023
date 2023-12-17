import sys

from aocd import get_data, submit

from util.grid import Grid, from_block, Pos, Dir, move, left, right

DAY = 16
YEAR = 2023


def part1(data: str) -> str:
    grid = from_block(data)
    start = 0, -1
    step(grid, start, Dir.E)
    hot = get_hot(grid)
    return str(hot)


def get_hot(grid: Grid) -> int:
    hot = 0
    for pos in grid.positions():
        if grid.meta(pos, "hot"):
            hot += 1
    return hot


def step(grid: Grid, pos: Pos, dir: Dir):
    next_pos = move(pos, dir)
    if not grid.inside(next_pos):
        return
    if grid.meta(next_pos, dir.value):
        return
    grid.mark(next_pos, "hot", True)
    grid.mark(next_pos, dir.value, True)
    symbol = grid.get(next_pos)
    next_dirs = [dir]
    if symbol == "/":
        if dir in [Dir.E, Dir.W]:
            next_dirs = [left(dir)]
        else:
            next_dirs = [right(dir)]
    elif symbol == "\\":
        if dir in [Dir.E, Dir.W]:
            next_dirs = [right(dir)]
        else:
            next_dirs = [left(dir)]
    elif symbol == "|" and dir in [Dir.E, Dir.W]:
        next_dirs = [Dir.N, Dir.S]
    elif symbol == "-" and dir in [Dir.S, Dir.N]:
        next_dirs = [Dir.E, Dir.W]
    for next_dir in next_dirs:
        step(grid, next_pos, next_dir)


def part2(data: str) -> str:
    grid = from_block(data)
    best = 0
    for i in range(grid.n):
        grid.reset_meta()
        start = i, -1
        step(grid, start, Dir.E)
        hot = get_hot(grid)
        best = max(best, hot)
        grid.reset_meta()
        start = i, grid.m
        step(grid, start, Dir.W)
        hot = get_hot(grid)
        best = max(best, hot)
    for j in range(grid.m):
        grid.reset_meta()
        start = -1, j
        step(grid, start, Dir.S)
        hot = get_hot(grid)
        best = max(best, hot)
        grid.reset_meta()
        start = grid.m, j
        step(grid, start, Dir.N)
        hot = get_hot(grid)
        best = max(best, hot)
    return str(best)


if __name__ == '__main__':
    sys.setrecursionlimit(1_000_000)
    input_data = get_data(day=DAY, year=YEAR)
    test_data = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""
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
