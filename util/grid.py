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


Pos = tuple[int, int]
PosDir = tuple[Pos, Dir]


def manhattan(p1: Pos, p2: Pos) -> int:
    y1, x1 = p1
    y2, x2 = p2
    return abs(y1 - y2) + abs(x1 - x2)


def right(d: Dir) -> Dir:
    if d == Dir.W:
        return Dir.N
    if d == Dir.N:
        return Dir.E
    if d == Dir.E:
        return Dir.S
    if d == Dir.S:
        return Dir.W


def left(d: Dir) -> Dir:
    if d == Dir.W:
        return Dir.S
    if d == Dir.N:
        return Dir.W
    if d == Dir.E:
        return Dir.N
    if d == Dir.S:
        return Dir.E


def turnaround(d: Dir) -> Dir:
    if d == Dir.W:
        return Dir.E
    if d == Dir.N:
        return Dir.S
    if d == Dir.E:
        return Dir.W
    if d == Dir.S:
        return Dir.N


def move(p: Pos, d: Dir, steps: int = 1) -> Pos:
    y, x = p
    if d == Dir.E:
        return y, x + steps
    if d == Dir.W:
        return y, x - steps
    if d == Dir.N:
        return y - steps, x
    if d == Dir.S:
        return y + steps, x


class Grid:

    def __init__(self, vals: Iterable[Iterable[S]], transform: Callable[[S], T] = lambda x: x):
        self.vals = [[transform(x) for x in row] for row in vals]
        self.n = len(self.vals)
        self.m = len(self.vals[0])
        self.metadata = defaultdict(dict)

    def get(self, p: Pos) -> T:
        y, x = p
        return self.vals[y][x]

    def set(self, p: Pos, val: T) -> None:
        if not self.inside(p):
            raise ValueError(f"{p} Out of grid.")
        y, x = p
        self.vals[y][x] = val

    def inside(self, p: Pos) -> bool:
        y, x = p
        return 0 <= y < self.n and 0 <= x < self.m

    def clamp(self, p: Pos) -> Pos:
        y, x = p
        return max(0, min(self.n - 1, y)), max(0, min(self.m - 1, x))

    def where(self, f: Callable[[T], bool]) -> list[Pos]:
        return [(y, x) for y in range(self.n) for x in range(self.m) if f(self.get((y, x)))]

    def mark(self, p: Pos, k: str, v: Any) -> None:
        self.metadata[p][k] = v

    def meta(self, p: Pos, k: str) -> Optional[Any]:
        return self.metadata[p].get(k)

    def reset_meta(self) -> None:
        self.metadata = defaultdict(dict)

    def positions(self) -> Iterator[Pos]:
        for i in range(self.n):
            for j in range(self.m):
                yield i, j

    def show(self, transform: Callable[[T], str] = str) -> str:
        res = ""
        for i in range(self.n):
            for j in range(self.m):
                res += transform(self.get((i, j)))
            res += "\n"
        return res


def from_block(data: str, transform: Callable[[str], T] = lambda x: x):
    return Grid(data.splitlines(), transform)
