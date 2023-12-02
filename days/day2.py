import re

from aocd import get_data, submit

DAY = 2
YEAR = 2023


#rgb order
def parse_games(data: str) -> list[list[list[int]]]:
    games = []
    for line in data.splitlines():
        prefix, game_text = line.split(":")
        game = []
        for round in game_text.split(";"):
            pulled = [0,0,0]
            for pull in round.split(","):
                number = int(re.search(r"\d+", pull).group())
                if "red" in pull:
                    pulled[0] += number
                elif "green" in pull:
                    pulled[1] += number
                elif "blue" in pull:
                    pulled[2] += number
                else:
                    raise ValueError("Unknown color")
            game.append(pulled)
        games.append(game)
    return games


def round_is_possible(round: list[int]) -> bool:
    return round[0] <= 12 and round[1] <= 13 and round[2] <= 14


def part1(data: str) -> str:
    games = parse_games(data)
    res = 0
    for index, game in enumerate(games, 1):
        if all(round_is_possible(round) for round in game):
            res += index
    return str(res)


def part2(data: str) -> str:
    games = parse_games(data)
    sum_of_products = 0
    for game in games:
        max_over_rounds = [
            max(round[i] for round in game)
            for i in range(3)
        ]
        sum_of_products += max_over_rounds[0] * max_over_rounds[1] * max_over_rounds[2]
    return str(sum_of_products)


if __name__ == '__main__':
    input_data = get_data(day=DAY, year=YEAR)
    ans1 = part1(input_data)
    print(ans1)
    # submit(answer=ans1, day=DAY, year=YEAR, part=1)
    ans2 = part2(input_data)
    print(ans2)
    submit(answer=ans2, day=DAY, year=YEAR, part=2)
