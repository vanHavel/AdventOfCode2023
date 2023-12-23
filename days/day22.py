import copy
import sys

from aocd import get_data, submit
from util.grid3 import *

DAY = 22
YEAR = 2023


def parse_grid(data: str) -> tuple[Grid, list[set[Pos]]]:
    lines = data.splitlines()
    xmax, ymax, zmax = 0, 0, 0
    cubes = []
    for index, line in enumerate(lines, start=1):
        start, end = line.split("~")
        start_cube = tuple(map(int, start.split(",")))
        end_cube = tuple(map(int, end.split(",")))
        ymax = max(xmax, start_cube[0], end_cube[0])
        xmax = max(ymax, start_cube[1], end_cube[1])
        zmax = max(zmax, start_cube[2], end_cube[2])
        cube = (index, start_cube, end_cube)
        cubes.append(cube)
    grid = Grid(((0 for k in range(0, zmax + 1)) for i in range(0, xmax + 1)) for j in range(0, ymax + 1))
    cubesets = []
    for cube in cubes:
        index, start_cube, end_cube = cube
        cubeset = set()
        for y in range(start_cube[0], end_cube[0] + 1):
            for x in range(start_cube[1], end_cube[1] + 1):
                for z in range(start_cube[2], end_cube[2] + 1):
                    grid.set((y, x, z), index)
                    cubeset.add((y, x, z))
        cubesets.append(cubeset)

    return grid, cubesets


def fall(grid: Grid, cubes: list[set[Pos]]) -> set[int]:
    change = True
    fallen = set()
    while change:
        change = False
        for index, cube in enumerate(cubes):
            cube_val = grid.get(next(iter(cube)))
            can_fall = True
            while can_fall:
                for pos in cube:
                    if pos[2] == 1 or grid.get((pos[0], pos[1], pos[2] - 1)) not in (0, cube_val):
                        can_fall = False
                        break
                if can_fall:
                    fallen.add(cube_val)
                    change = True
                    for pos in cube:
                        grid.set(pos, 0)
                    for pos in cube:
                        grid.set((pos[0], pos[1], pos[2] - 1), cube_val)
                    cube = set((pos[0], pos[1], pos[2] - 1) for pos in cube)
            cubes[index] = cube
    return fallen


def part1(data: str) -> str:
    grid, cubes = parse_grid(data)
    fall(grid, cubes)
    cube_supports = defaultdict(set)
    cube_supported_by = defaultdict(set)
    for cube in cubes:
        cube_val = grid.get(next(iter(cube)))
        for pos in cube:
            below = move(pos, Dir.D)
            if grid.inside(below) and grid.get(below) not in (0, cube_val):
                cube_supported_by[cube_val].add(grid.get(below))
                cube_supports[grid.get(below)].add(cube_val)
    ans = 0
    for cube in cubes:
        cube_val = grid.get(next(iter(cube)))
        supports = cube_supports[cube_val]
        ok = True
        for support in supports:
            if len(cube_supported_by[support]) == 1:
                ok = False
                break
        if ok:
            ans += 1
    return str(ans)


def part2(data: str) -> str:
    grid, cubes = parse_grid(data)
    fall(grid, cubes)
    ans = 0
    for cube in cubes:
        gridcube = copy.deepcopy(grid)
        for pos in cube:
            gridcube.set(pos, 0)
        fallen = fall(gridcube, [acube for acube in cubes if acube != cube])
        ans += len(fallen)
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
