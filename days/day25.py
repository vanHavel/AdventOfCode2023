import sys

import matplotlib.pyplot
from aocd import get_data, submit
import networkx as nx

DAY = 25
YEAR = 2023


def part1(data: str) -> str:
    lines = data.splitlines()
    edges = list()
    for line in lines:
        left, rights = line.split(":")
        left = left.strip()
        for right in rights.split():
            right = right.strip()
            edges.append((left, right))
    g = nx.Graph(edges)
    nx.draw_networkx(g, with_labels=True)
    matplotlib.pyplot.show()
    edges_to_remove = [("pjj", "dlk"), ("pcc", "htj"), ("htb", "bbg")]
    g.remove_edges_from(edges_to_remove)
    components = nx.connected_components(g)
    c1, c2 = components
    ans = len(c1) * len(c2)
    return str(ans)


if __name__ == '__main__':
    sys.setrecursionlimit(1_000_000)
    input_data = get_data(day=DAY, year=YEAR)
    ans = part1(input_data)
    print(ans)
    # submit(answer=ans1, day=DAY, year=YEAR, part=1)
