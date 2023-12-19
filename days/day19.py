import sys
from collections import defaultdict

from aocd import get_data, submit
from joblib import Parallel, delayed

DAY = 19
YEAR = 2023


def parse_flows(flows: str) -> tuple[dict[str, list], dict[str, list]]:
    workflows = {}
    stops = defaultdict(list)
    for flow in flows.splitlines():
        key, val = flow.split("{")
        val = val[:-1]
        rules = val.split(",")
        workflows[key] = []
        for rule in rules:
            if ":" not in rule:
                workflows[key].append(rule)
            else:
                condition, target = rule.split(":")
                checked = condition[0]
                operator = condition[1]
                value = int(condition[2:])
                stops[checked].append(value if operator == "<" else value + 1)
                workflows[key].append((checked, operator, value, target))
    for key in stops:
        stops[key].append(1)
        stops[key].append(4_001)
        stops[key] = sorted(list(set(stops[key])))
        stops[key] = [(stops[key][i], stops[key][i + 1] - 1) for i in range(len(stops[key]) - 1)]
    return workflows, stops


def part1(data: str) -> str:
    flows, ps = data.split("\n\n")
    workflows, stops = parse_flows(flows)
    parts = []
    for p in ps.splitlines():
        part = {}
        for equationn in p[1:-1].split(","):
            key, value = equationn.split("=")
            part[key] = int(value)
        parts.append(part)
    ans = 0
    for part in parts:
        ans += simulate(workflows, part, "in")
    return str(ans)


def simulate(workflows: dict[str, list], part: dict[str, int], flow: str) -> int:
    if flow == "A":
        return sum(part.values())
    if flow == "R":
        return 0
    rules = workflows[flow]
    for rule in rules:
        if isinstance(rule, str):
            return simulate(workflows, part, rule)
        else:
            checked, operator, value, target = rule
            if operator == ">":
                if part[checked] > value:
                    return simulate(workflows, part, target)
            elif operator == "<":
                if part[checked] < value:
                    return simulate(workflows, part, target)


def part2(data: str) -> str:
    flows, _ = data.split("\n\n")
    workflows, stops = parse_flows(flows)

    def _inner(arange):
        ans = 0
        for xrange in stops["x"]:
            for mrange in stops["m"]:
                for srange in stops["s"]:
                    part = {"a": arange[1], "x": xrange[1], "m": mrange[1], "s": srange[1]}
                    if simulate(workflows, part, "in"):
                        sdiff = srange[1] - srange[0] + 1
                        mdiff = mrange[1] - mrange[0] + 1
                        xdiff = xrange[1] - xrange[0] + 1
                        adiff = arange[1] - arange[0] + 1
                        ans += sdiff * mdiff * xdiff * adiff
        return ans

    res = Parallel(n_jobs=8, return_as="generator")(delayed(_inner)(arange) for arange in stops["a"])
    ans = sum(res)

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
