from aocd import get_data, submit

DAY = 9
YEAR = 2023


def part1(data: str) -> tuple[str, str]:
    lines = data.splitlines()
    res1, res2 = 0, 0
    for line in lines:
        nums = list(map(int, line.split()))
        lasts = []
        firsts = []
        ok = False
        while not ok:
            lasts.append(nums[-1])
            firsts.append(nums[0])
            pairs = list(zip(nums[:-1], nums[1:]))
            diffs = [p[1] - p[0] for p in pairs]
            if all([d == 0 for d in diffs]):
                res1 += sum(lasts)
                news = []
                diff = 0
                for f in reversed(firsts):
                    news.append(f - diff)
                    diff = f - diff
                res2 += news[-1]
                ok = True
            else:
                nums = diffs
    return str(res1), str(res2)


if __name__ == '__main__':
    input_data = get_data(day=DAY, year=YEAR)
    ans1, ans2 = part1(input_data)
    print(ans1)
    # submit(answer=ans1, day=DAY, year=YEAR, part=1)
    print(ans2)
    # submit(answer=ans2, day=DAY, year=YEAR, part=2)
