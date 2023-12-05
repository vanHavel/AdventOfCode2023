from typing import Optional

from aocd import get_data, submit

DAY = 5
YEAR = 2023


def parse(data: str) -> tuple[list[int], list[list[list[int]]]]:
    initial, *rest = data.split("\n\n")
    seeds = [int(x) for x in initial.split(": ")[1].split()]
    maps = []
    for part in rest:
        current_map = []
        numbers = part.split(":\n")[1]
        for row in numbers.splitlines():
            current_map.append([int(x) for x in row.split()])
        maps.append(current_map)
    return seeds, maps


def transform(seed: int, map: list[list[int]]) -> int:
    for destination, source, size in map:
        if source <= seed < source + size:
            return destination + seed - source
    return seed


def part1(data: str) -> str:
    seeds, maps = parse(data)
    for map in maps:
        seeds = [transform(seed, map) for seed in seeds]
    return str(min(seeds))


def part2(data: str) -> str:
    seeds, maps = parse(data)
    odd, even = seeds[::2], seeds[1::2]
    seed_ranges = [(left, left + size - 1) for left, size in zip(odd, even)]
    for map in maps:
        seed_ranges = [range for seed_range in seed_ranges for range in transform_range(seed_range, map)]
    return str(min(seed_ranges, key=lambda x: x[0])[0])


def intersect_range(range1: tuple[int, int], range2: tuple[int, int]) -> Optional[tuple[int, int]]:
    left = max(range1[0], range2[0])
    right = min(range1[1], range2[1])
    if left <= right:
        return left, right
    else:
        return None


def transform_range(seed_range: tuple[int, int], map: list[list[int]]) -> list[tuple[int, int]]:
    res = []
    covered = []
    for destination, source, size in map:
        map_source_range = source, source + size - 1
        intersection = intersect_range(seed_range, map_source_range)
        if intersection:
            delta_intersection = intersection[0] - source, intersection[1] - source
            res.append((destination + delta_intersection[0], destination + delta_intersection[1]))
            covered.append(intersection)
    covered = sorted(covered, key=lambda x: x[0])
    pointer = seed_range[0]
    for range in covered:
        if range[0] > pointer:
            res.append((pointer, range[0] - 1))
        pointer = range[1] + 1
    if pointer <= seed_range[1]:
        res.append((pointer, seed_range[1]))
    return res


if __name__ == '__main__':
    input_data = get_data(day=DAY, year=YEAR)
    ans1 = part1(input_data)
    print(ans1)
    # submit(answer=ans1, day=DAY, year=YEAR, part=1)
    ans2 = part2(input_data)
    print(ans2)
    # submit(answer=ans2, day=DAY, year=YEAR, part=2)