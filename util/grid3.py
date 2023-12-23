from collections import defaultdict
from enum import Enum
from typing import Any, TypeVar, Iterable, Callable, Optional, Iterator

T = TypeVar("T")
S = TypeVar("S")


class Dir(Enum):
    N = "N"
    E = "E"
    S = "S"
    W = "W"
    U = "U"
    D = "D"


Pos = tuple[int, int, int]
PosDir = tuple[Pos, Dir]


def manhattan(p1: Pos, p2: Pos) -> int:
    y1, x1, z1 = p1
    y2, x2, z2 = p2
    return abs(y1 - y2) + abs(x1 - x2) + abs(z1 - z2)


def right(d: Dir) -> Dir:
    if d == Dir.W:
        return Dir.N
    if d == Dir.N:
        return Dir.E
    if d == Dir.E:
        return Dir.S
    if d == Dir.S:
        return Dir.W
    else:
        return d


def left(d: Dir) -> Dir:
    if d == Dir.W:
        return Dir.S
    if d == Dir.N:
        return Dir.W
    if d == Dir.E:
        return Dir.N
    if d == Dir.S:
        return Dir.E
    else:
        return d


def turnaround(d: Dir) -> Dir:
    if d == Dir.W:
        return Dir.E
    if d == Dir.N:
        return Dir.S
    if d == Dir.E:
        return Dir.W
    if d == Dir.S:
        return Dir.N
    else:
        return d


def move(p: Pos, d: Dir, steps: int = 1) -> Pos:
    y, x, z = p
    if d == Dir.E:
        return y, x + steps, z
    if d == Dir.W:
        return y, x - steps, z
    if d == Dir.N:
        return y - steps, x, z
    if d == Dir.S:
        return y + steps, x, z
    if d == Dir.U:
        return y, x, z + steps
    if d == Dir.D:
        return y, x, z - steps


class Grid:

    def __init__(self, vals: Iterable[Iterable[Iterable[S]]], transform: Callable[[S], T] = lambda x: x):
        self.vals = [[[transform(x) for x in col] for col in block] for block in vals]
        self.n = len(self.vals)
        self.m = len(self.vals[0])
        self.h = len(self.vals[0][0])
        self.metadata = defaultdict(dict)

    def get(self, p: Pos) -> T:
        y, x, z = p
        return self.vals[y][x][z]

    def set(self, p: Pos, val: T) -> None:
        if not self.inside(p):
            raise ValueError(f"{p} Out of grid.")
        y, x, z = p
        self.vals[y][x][z] = val

    def inside(self, p: Pos) -> bool:
        y, x, z = p
        return 0 <= y < self.n and 0 <= x < self.m and 0 <= z < self.h

    def clamp(self, p: Pos) -> Pos:
        y, x, z = p
        return max(0, min(self.n - 1, y)), max(0, min(self.m - 1, x)), max(0, min(self.h - 1, z))

    def where(self, f: Callable[[T], bool]) -> list[Pos]:
        return [(y, x, z) for y in range(self.n) for x in range(self.m) for z in range(self.h) if f(self.get((y, x, z)))]

    def mark(self, p: Pos, k: str, v: Any) -> None:
        self.metadata[p][k] = v

    def meta(self, p: Pos, k: str) -> Optional[Any]:
        return self.metadata[p].get(k)

    def reset_meta(self) -> None:
        self.metadata = defaultdict(dict)

    def positions(self) -> Iterator[Pos]:
        for i in range(self.n):
            for j in range(self.m):
                for k in range(self.h):
                    yield i, j, k

    def show(self, transform: Callable[[T], str] = str) -> str:
        res = ""
        for k in range(self.h):
            res += f"z={k}\n"
            for i in range(self.n):
                for j in range(self.m):
                    res += transform(self.get((i, j, k)))
                res += "\n"
        return res

