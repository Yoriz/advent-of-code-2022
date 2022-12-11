import dataclasses
import math
import operator
import typing

FILENAME = "day11_data.txt"


def yield_lines(filename: str) -> typing.Iterator[str]:
    with open(file=filename, mode="r") as read_file:
        for line in read_file:
            yield line.rstrip()


MonkeyId = int
ItemWorry = int

opperator_mapping = {"+": operator.add, "*": operator.mul}


def divisible_by(amount: int, divisible_amount: int) -> bool:
    return amount % divisible_amount == 0


@dataclasses.dataclass
class Operation:
    operator_symbol: str
    change_amount: typing.Optional[int] = None

    def worry_level_change(self, item_worry: ItemWorry) -> ItemWorry:
        change_amount = self.change_amount or item_worry
        operator = opperator_mapping[self.operator_symbol]
        return operator(item_worry, change_amount)


@dataclasses.dataclass
class Test:
    divisible_by_amount: int
    monkey_id_if_true: MonkeyId
    monkey_id_if_false: MonkeyId

    def monkey_id_to_throw_to(self, item_worry: ItemWorry) -> MonkeyId:
        return (
            self.monkey_id_if_true
            if divisible_by(item_worry, self.divisible_by_amount)
            else self.monkey_id_if_false
        )


@dataclasses.dataclass
class ThrownItem:
    item_worry: ItemWorry
    to_monkey_id: MonkeyId


@dataclasses.dataclass
class Monkey:
    id: MonkeyId
    operation: Operation
    test: Test
    starting_items: list[ItemWorry] = dataclasses.field(default_factory=list)
    inspected_item_count: int = dataclasses.field(default=0, init=False)

    def has_starting_items(self) -> bool:
        return bool(self.starting_items)

    def catch_thrown_item(self, thrown_item: ThrownItem) -> None:
        self.starting_items.append(thrown_item.item_worry)

    def inspect_and_throw_items(self) -> typing.Iterator[ThrownItem]:
        for item_worry in self.starting_items[:]:
            self.inspected_item_count += 1
            self.starting_items.pop(0)
            item_worry = self.operation.worry_level_change(item_worry)
            item_worry = math.floor(item_worry / 3)
            to_monkey_id = self.test.monkey_id_to_throw_to(item_worry)
            yield ThrownItem(item_worry, to_monkey_id)


def extract_monkey_id(line: str) -> MonkeyId:
    _, monkey = line.split(" ")
    return int(monkey[0])


def extract_starting_items(line: str) -> list[int]:
    _, items = line.split("  Starting items: ")
    items = items.split(",")

    return [int(item.strip()) for item in items]


def extract_operation(line: str) -> Operation:
    _, items = line.split("  Operation: new = old ")
    operator_symbol, change_amount = items.split(" ")
    change_amount = None if change_amount == "old" else int(change_amount)
    return Operation(operator_symbol, change_amount)


def extract_test(line1: str, line2: str, line3: str) -> Test:
    _, divisible_by_amount = line1.split("  Test: divisible by ")
    _, monkey_id_if_true = line2.split("    If true: throw to monkey ")
    _, monkey_id_if_false = line3.split("If false: throw to monkey ")
    return Test(
        int(divisible_by_amount), int(monkey_id_if_true), int(monkey_id_if_false)
    )


def create_monkeys(lines: typing.Iterator[str]) -> list[Monkey]:
    monkeys: list[Monkey] = []
    while True:
        monkey_id = extract_monkey_id(next(lines))
        starting_items = extract_starting_items(next(lines))
        operation = extract_operation(next(lines))
        test = extract_test(next(lines), next(lines), next(lines))
        monkeys.append(Monkey(monkey_id, operation, test, starting_items))
        try:
            next(lines)
        except StopIteration:
            break
    return monkeys


@dataclasses.dataclass
class KeepAwayGame:
    monkeys: list[Monkey] = dataclasses.field(default_factory=list)

    def play_round(self) -> None:
        for monkey in self.monkeys:
            if not monkey.has_starting_items():
                continue
            for thrown_item in monkey.inspect_and_throw_items():
                self.monkeys[thrown_item.to_monkey_id].catch_thrown_item(thrown_item)

    def monkey_items(self) -> str:
        string = ""
        for monkey in self.monkeys:
            string = f"{string}Monkey {monkey.id}: {monkey.starting_items}\n"

        return string

    def monkey_inspected_item_counts(self) -> list[int]:
        return [monkey.inspected_item_count for monkey in self.monkeys]


def part1(filename: str) -> None:
    lines = yield_lines(filename)
    monkeys = create_monkeys(lines)
    keep_away_game = KeepAwayGame(monkeys)
    round = 0
    for round in range(20):
        keep_away_game.play_round()
    print(
        f"After round {round+1}, the monkeys are holding items with these worry levels:"
    )
    print(keep_away_game.monkey_items())
    inspection_counts = sorted(keep_away_game.monkey_inspected_item_counts())
    print(inspection_counts[-2] * inspection_counts[-1])


def part2(filename: str) -> None:
    lines = yield_lines(filename)


def main():
    part1(FILENAME)
    # part2(FILENAME)


if __name__ == "__main__":
    main()
