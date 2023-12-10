from aocd import get_data, submit

DAY = 10
YEAR = 2023


def turn_right(dir: str) -> str:
    if dir == "N":
        return "E"
    elif dir == "E":
        return "S"
    elif dir == "S":
        return "W"
    elif dir == "W":
        return "N"


def turn_left(dir: str) -> str:
    return turn_right(turn_right(turn_right(dir)))


def advance(pos: tuple[int, int], dir: str) -> tuple[int, int]:
    y, x = pos
    if dir == "N":
        return y - 1, x
    elif dir == "E":
        return y, x + 1
    elif dir == "S":
        return y + 1, x
    elif dir == "W":
        return y, x - 1


def move(field: str, pos: tuple[int, int], dir: str) -> tuple[int, int, str]:
    y, x = pos
    if dir == "N":
        if field == "|":
            return y - 1, x, "N"
        elif field == "F":
            return y, x + 1, "E"
        elif field == "7":
            return y, x - 1, "W"
    elif dir == "S":
        if field == "|":
            return y + 1, x, "S"
        elif field == "L":
            return y, x + 1, "E"
        elif field == "J":
            return y, x - 1, "W"
    elif dir == "W":
        if field == "-":
            return y, x - 1, "W"
        elif field == "F":
            return y + 1, x, "S"
        elif field == "L":
            return y - 1, x, "N"
    elif dir == "E":
        if field == "-":
            return y, x + 1, "E"
        elif field == "J":
            return y - 1, x, "N"
        elif field == "7":
            return y + 1, x, "S"


def floodfill(marks: dict[tuple[int, int], str], grid: list[str], pos: tuple[int, int]):
    m = len(grid[0])
    n = len(grid)
    y, x = pos
    if y < 0 or y >= n or x < 0 or x >= m:
        return
    if marks.get(pos) in ["P", "K"]:
        return
    marks[pos] = "K"
    for dir in "NSEW":
        next = advance(pos, dir)
        floodfill(marks, grid, next)


def parts(data: str) -> tuple[str, str]:
    grid = data.splitlines()
    marks = dict()
    m = len(grid[0])
    n = len(grid)

    # find start
    ok = False
    for sy in range(n):
        for sx in range(m):
            if grid[sy][sx] == "S":
                ok = True
                break
        if ok:
            break

    # handle start
    marks[(sy, sx)] = "P"
    d = "S"
    marks[advance((sy, sx), turn_right(d))] = "O"
    marks[advance((sy, sx), turn_left(d))] = "I"

    # iterate
    moves = 1
    y, x = sy + 1, sx
    while (y, x) != (sy, sx):
        cy, cx = y, x
        # mark pipe
        marks[(y, x)] = "P"
        # mark in and out
        pr = advance((y, x), turn_right(d))
        pl = advance((y, x), turn_left(d))
        if marks.get(pr) != "P":
            marks[pr] = "O"
        if marks.get(pl) != "P":
            marks[pl] = "I"
        # move
        moves += 1
        y, x, d = move(grid[y][x], (y, x), d)
        # mark in and out again (for curves)
        pr = advance((cy, cx), turn_right(d))
        pl = advance((cy, cx), turn_left(d))
        if marks.get(pr) != "P":
            marks[pr] = "O"
        if marks.get(pl) != "P":
            marks[pl] = "I"

    # determine in and out
    min_i = min([pos[0] for pos in marks if marks[pos] == "I"])
    min_o = min([pos[0] for pos in marks if marks[pos] == "O"])
    if min_i < min_o:
        for pos in marks:
            if marks[pos] == "I":
                marks[pos] = "O"
            elif marks[pos] == "O":
                marks[pos] = "I"

    # fill inside
    tofill = [pos for pos in marks if marks[pos] == "I"]
    for pos in tofill:
        floodfill(marks, grid, pos)
    internal = sum([1 for pos in marks if marks[pos] == "K"])

    # print grid
    gs = ""
    for i in range(n):
        for j in range(m):
            if (i, j) in marks:
                gs += marks[(i, j)]
            else:
                gs += grid[i][j]
        gs += "\n"
    print(gs)

    return str(moves // 2), str(internal)


if __name__ == '__main__':
    input_data = get_data(day=DAY, year=YEAR)
    ans1, ans2 = parts(input_data)
    print(ans1)
    # submit(answer=ans1, day=DAY, year=YEAR, part=1)
    print(ans2)
    # submit(answer=ans2, day=DAY, year=YEAR, part=2)
