from dataclasses import astuple, dataclass, field
from queue import PriorityQueue
from typing import Callable, Dict, Iterable, List, Optional, Set, Tuple, TypeVar

S = TypeVar('S')


@dataclass(order=True)
class PrioritizedState:
    priority: int
    state: S = field(compare=False)


class AStar:
    def __init__(
        self,
        succ: Callable[[S], Iterable[Tuple[int, S]]],
        goal: Callable[[S], bool],
        h: Callable[[S], int]
    ):
        self.succ = succ
        self.goal = goal
        self.h = h

    def search(self, start: S) -> Optional[Tuple[int, List[S]]]:
        costs = {start: 0}
        preds: Dict[S, S] = {}
        closed: Set[S] = set()
        pq: PriorityQueue[PrioritizedState] = PriorityQueue()
        pq.put(PrioritizedState(priority=0, state=start))

        while not pq.empty():
            top = pq.get()
            f, u = top.priority, top.state
            if u in closed:
                continue
            closed.add(u)

            if self.goal(u):
                path = [u]
                cur = u
                while cur in preds:
                    path.append(preds[cur])
                    cur = preds[cur]
                return f, list(reversed(path))

            for d, v in self.succ(u):
                if v in closed:
                    continue

                g = costs[u] + d
                if v not in costs or costs[v] > g:
                    costs[v] = g
                    preds[v] = u
                    f = g + self.h(v)
                    pq.put(PrioritizedState(priority=f, state=v))

        return None


