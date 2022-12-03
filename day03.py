import dataclasses
from typing import Iterator
import typing
import enum
import itertools

FILENAME = "day3_data.txt"


class PriorityShift(enum.IntEnum):
    LOWERCASE = 96
    UPPERCASE = 38


def yield_data(filename: str) -> Iterator[str]:
    with open(file=filename, mode="r") as read_file:
        for line in read_file:
            yield line.strip()


def split_string_in_half(string: str) -> tuple[str, str]:
    string_length = len(string) // 2
    return string[:string_length], string[string_length:]


def common_items(items: typing.Sequence[typing.Sequence]) -> set:
    return set(items[0]).intersection(*items[1:])


def rucksack_item_priority(item: str) -> int:
    shift = PriorityShift.LOWERCASE if item.islower() else PriorityShift.UPPERCASE
    return ord(item) - shift


@dataclasses.dataclass
class Comparment:
    items: str


@dataclasses.dataclass
class RuckShack:
    compartments: list[Comparment] = dataclasses.field(default_factory=list)

    def compartments_common_item(self):
        return common_items([compartment.items for compartment in self.compartments])

    def all_items(self) -> str:
        return "".join(compartment.items for compartment in self.compartments)


def create_badly_packed_rucksacks(lines: Iterator[str]) -> Iterator[RuckShack]:
    for line in lines:
        first_half, secound_half = split_string_in_half(line)
        rucksack = RuckShack(
            compartments=[Comparment(first_half), Comparment(secound_half)]
        )
        yield rucksack


def sum_rucksacks_prioritys(rucksacks: Iterator[RuckShack]) -> int:
    priority_score_sum = 0
    for rucksack in rucksacks:
        rucksack: RuckShack
        for priority_item in rucksack.compartments_common_item():
            priority_score_sum += rucksack_item_priority(priority_item)
    return priority_score_sum


def grouper(
    iterable: typing.Iterable, n: int, fillvalue=None
):  # from itertools recipes
    "Collect data into non-overlapping fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)


def group_rucksacks(rucksacks: Iterator[RuckShack], group_size: int):
    return grouper(rucksacks, group_size)


def sum_rucksack_group_prioritys(rucksack_groups: Iterator[tuple[RuckShack]]):
    priority_score_sum = 0
    for rucksack_group in rucksack_groups:
        rucksack_group: tuple[RuckShack]
        rucksack_common_items = common_items(
            [rucksack.all_items() for rucksack in rucksack_group]
        )
        for priority_item in rucksack_common_items:
            priority_score_sum += rucksack_item_priority(priority_item)
    return priority_score_sum


def main():
    lines = yield_data(FILENAME)
    print(sum_rucksacks_prioritys(create_badly_packed_rucksacks(lines)))

    lines = yield_data(FILENAME)
    rucksack_groups = group_rucksacks(create_badly_packed_rucksacks(lines), 3)
    print(sum_rucksack_group_prioritys(rucksack_groups))


if __name__ == "__main__":
    main()
