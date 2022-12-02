from dataclasses import dataclass, field
from operator import methodcaller
from typing import Iterator

FILENAME = "day1_data.txt"


def yield_data(filename: str) -> Iterator[str]:
    with open(file=filename, mode="r") as read_file:
        for line in read_file:
            yield line.strip()


@dataclass
class Calorie:
    food_calories: list[int] = field(default_factory=list)

    def sum(self) -> int:
        return sum(self.food_calories)


def create_calories(data: Iterator[str]) -> list[Calorie]:
    calories: list[Calorie] = []
    calorie = Calorie()
    for line in data:
        if not line:
            calories.append(calorie)
            calorie = Calorie()
        else:
            calorie.food_calories.append(int(line))
    calories.append(calorie)
    return calories


def get_max_calorie(calories: list[Calorie]) -> Calorie:
    max_calorie = calories[0]
    for calorie in calories[1:]:
        if calorie.sum() > max_calorie.sum():
            max_calorie = calorie
    return max_calorie


def get_top_three_calories(calories: list[Calorie]) -> list[Calorie]:
    top_three_calories: list[Calorie] = []
    for calorie in calories:
        top_three_calories.append(calorie)
        top_three_calories.sort(key=methodcaller("sum"))
        top_three_calories = top_three_calories[-3:]
    return top_three_calories


def main():
    data = yield_data(FILENAME)
    calories = create_calories(data)
    top_three_calories = get_top_three_calories(calories)
    total = sum(calorie.sum() for calorie in top_three_calories)
    print(f"{total=}")


if __name__ == "__main__":
    main()
