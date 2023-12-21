import sys
from queue import Queue

from aocd import get_data, submit
from util.grid import *

DAY = 21
YEAR = 2023


def part1(data: str) -> str:
    grid = from_block(data)
    start = grid.where(lambda x: x == "S")[0]
    reachable = defaultdict(set)
    reachable[0] = {start}
    max_steps = 64
    q = Queue()
    q.put((start, 0))
    while not q.empty():
        pos, steps = q.get()
        for dir in Dir:
            next = move(pos, dir)
            if grid.inside(next) and grid.get(next) != "#" and next not in reachable[steps+1] and steps < max_steps:
                reachable[steps+1].add(next)
                q.put((next, steps + 1))

    return str(len(reachable[max_steps]))


def part2(data: str) -> str:
    lines = data.splitlines()
    factor = 1000 // len(lines)
    big_lines = [line * factor for line in lines] * factor
    grid = from_block("\n".join(big_lines))
    starts = grid.where(lambda x: x == "S")
    xs, ys = [p[1] for p in starts], [p[0] for p in starts]
    real_start = sorted(ys)[len(ys) // 2], sorted(xs)[len(xs) // 2]
    for pos in starts:
        if pos != real_start:
            grid.set(pos, ".")
    reachable = defaultdict(set)
    reachable[0] = {real_start}
    max_steps = 500
    q = Queue()
    q.put((real_start, 0))
    while not q.empty():
        pos, steps = q.get()
        for dir in Dir:
            next = move(pos, dir)
            if grid.inside(next) and grid.get(next) != "#" and next not in reachable[steps + 1] and steps < max_steps:
                reachable[steps + 1].add(next)
                q.put((next, steps + 1))
    diffs = [len(reachable[i+1]) - len(reachable[i]) for i in range(max_steps - 1)]
    target = 26501365
    for start in range(50):
        for length in range(3, 150):
            ok = True
            for i in range(length):
                a1 = diffs[start+i]
                a2 = diffs[start+length+i]
                a3 = diffs[start+2*length+i]
                if a3 - a2 != a2 - a1:
                    ok = False
                    break
            if ok:
                res = len(reachable[start])
                cycle_diffs = diffs[start:start+length]
                diff_growths = [diffs[start+length+i] - diffs[start+i] for i in range(length)]
                target -= start
                for i in range(target):
                    res += cycle_diffs[i % len(cycle_diffs)]
                    cycle_diffs[i % len(cycle_diffs)] += diff_growths[i % len(cycle_diffs)]
                return str(res)


if __name__ == '__main__':
    sys.setrecursionlimit(1_000_000)
    input_data = get_data(day=DAY, year=YEAR)
    ans1 = part1(input_data)
    print(ans1)
    # submit(answer=ans1, day=DAY, year=YEAR, part=1)
    ans2 = part2(input_data)
    print(ans2)
    # submit(answer=ans2, day=DAY, year=YEAR, part=2)
