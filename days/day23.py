import sys
from queue import Queue

from aocd import get_data, submit

from util.grid import *

DAY = 23
YEAR = 2023


def part1(data: str) -> str:
    grid = from_block(data)
    for i in range(grid.m):
        if grid.get((0, i)) == ".":
            start = (0, i)
        if grid.get((grid.n - 1, i)) == ".":
            end = (grid.n - 1, i)
    dists = defaultdict(lambda: -1)
    q = Queue()
    q.put((start, start, 0))
    while not q.empty():
        pos, prev, dist = q.get()
        if dists[pos] < dist:
            dists[pos] = dist
            if grid.get(pos) == ">":
                q.put((move(pos, Dir.E), pos, dist + 1))
            elif grid.get(pos) == "<":
                q.put((move(pos, Dir.W), pos, dist + 1))
            elif grid.get(pos) == "^":
                q.put((move(pos, Dir.N), pos, dist + 1))
            elif grid.get(pos) == "v":
                q.put((move(pos, Dir.S), pos, dist + 1))
            else:
                for dir in Dir:
                    next = move(pos, dir)
                    if not grid.inside(next):
                        continue
                    if grid.get(next) == ">" and dir == Dir.W:
                        continue
                    if grid.get(next) == "<" and dir == Dir.E:
                        continue
                    if grid.get(next) == "^" and dir == Dir.S:
                        continue
                    if grid.get(next) == "v" and dir == Dir.N:
                        continue
                    if next != prev and grid.get(next) != "#":
                        q.put((next, pos, dist + 1))
    return str(dists[end])


def part2(data: str) -> str:
    grid = from_block(data)
    for pos in grid.positions():
        if grid.get(pos) not in ".#":
            grid.set(pos, ".")
    for i in range(grid.m):
        if grid.get((0, i)) == ".":
            start = (0, i)
        if grid.get((grid.n - 1, i)) == ".":
            end = (grid.n - 1, i)

    nodes = [start]
    edges = []

    def dfs(pos: Pos, initial_dir: Dir) -> None:
        prev = pos
        cur = move(pos, initial_dir)
        steps = 1
        while True:
            moves = []
            for dir in Dir:
                next = move(cur, dir)
                if grid.inside(next) and grid.get(next) == "." and next != prev:
                    moves.append(dir)
            if len(moves) == 0:
                if cur == end:
                    nodes.append(end)
                    edges.append((pos, end, steps))
                return
            elif len(moves) == 1:
                prev = cur
                cur = move(cur, moves[0])
                steps += 1
            else:
                if (pos, cur, steps) not in edges and (cur, pos, steps) not in edges:
                    edges.append((pos, cur, steps))
                if cur not in nodes:
                    nodes.append(cur)
                    for dir in moves:
                        dfs(cur, dir)
                return
    dfs(start, Dir.S)
    adj = defaultdict(set)
    for (a, b, dist) in edges:
        adj[a].add((b, dist))
        adj[b].add((a, dist))

    def backtrack(pos: Pos, path: list[Pos]) -> int:
        if pos == end:
            return 0
        best = -1
        for (next, dist) in adj[pos]:
            if next not in path:
                path.append(next)
                res = backtrack(next, path)
                if res != -1:
                    best = max(best, res + dist)
                path.pop()
        return best

    ans = backtrack(start, [start])
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
