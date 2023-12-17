import sys

from aocd import get_data, submit
from util.astar import AStar
from util.grid import *

DAY = 17
YEAR = 2023


def part1(data: str) -> str:
    grid = from_block(data, int)
    goalpos = (grid.n - 1, grid.m - 1)
    startpos = (0, 0)
    astar = AStar(
        succ=lambda posdir: succs(grid, posdir, minmoves=1, maxmoves=3),
        goal=lambda posdir: posdir[0] == goalpos,
        h=lambda posdir: manhattan(posdir[0], goalpos)
    )
    cost1, _ = astar.search((startpos, Dir.S))
    cost2, _ = astar.search((startpos, Dir.E))
    return str(min(cost1, cost2))


def succs(grid: Grid, posdir: PosDir, minmoves: int, maxmoves: int) -> Iterable[tuple[int, PosDir]]:
    cpos, cdir = posdir
    for dir in [left(cdir), right(cdir)]:
        npos = cpos
        cost = 0
        for i in range(1, maxmoves + 1):
            npos = move(npos, dir)
            if grid.inside(npos):
                cost += grid.get(npos)
                if i >= minmoves:
                    yield cost, (npos, dir)


def part2(data: str) -> str:
    grid = from_block(data, int)
    goalpos = (grid.n - 1, grid.m - 1)
    startpos = (0, 0)
    astar = AStar(
        succ=lambda posdir: succs(grid, posdir, minmoves=4, maxmoves=10),
        goal=lambda posdir: posdir[0] == goalpos,
        h=lambda posdir: manhattan(posdir[0], goalpos)
    )
    cost1, _ = astar.search((startpos, Dir.S))
    cost2, _ = astar.search((startpos, Dir.E))
    return str(min(cost1, cost2))


if __name__ == '__main__':
    sys.setrecursionlimit(1_000_000)
    input_data = get_data(day=DAY, year=YEAR)
    test_data = r"""2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""
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
