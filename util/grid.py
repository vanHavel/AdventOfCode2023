from typing import TypeVar, Iterable

T = TypeVar("T")


class Grid:

    def __init__(self, vals: Iterable[Iterable[T]]):
        self.vals = [[x for x in row] for row in vals]

    def get(self, i: int, j: int) -> T:
        return self.vals[i][j]

    def set(self, i: int, j: int, val: T):
        self.vals[i][j] = T


def from_block(data: str):
    return Grid(data.splitlines())
