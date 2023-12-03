import re

from aocd import get_data, submit

DAY = 3
YEAR = 2023


def parts(data: str) -> tuple[str, str]:
    res, gears = 0, 0
    gear_pos = {}
    grid = data.splitlines()
    rows = len(grid)
    for row, line in enumerate(grid):
        cols = len(line)
        current_num = ""
        for col, char in enumerate(line + "."):
            if char.isdigit():
                current_num += char
            elif current_num:
                ok = False
                for i in range(row-1, row+2):
                    for j in range(col-len(current_num) - 1, col+1):
                        i = max(0, min(i, rows - 1))
                        j = max(0, min(j, cols - 1))
                        if not grid[i][j].isdigit() and grid[i][j] != ".":
                            ok = True
                            if grid[i][j] == "*":
                                if (i, j) not in gear_pos:
                                    gear_pos[(i, j)] = int(current_num)
                                else:
                                    gears += gear_pos[(i, j)] * int(current_num)
                if ok:
                    res += int(current_num)
                current_num = ""
    return str(res), str(gears)


if __name__ == '__main__':
    input_data = get_data(day=DAY, year=YEAR)
    ans1, ans2 = parts(input_data)
    print(ans1, ans2)
    # submit(answer=ans1, day=DAY, year=YEAR, part=1)
    submit(answer=ans2, day=DAY, year=YEAR, part=2)
