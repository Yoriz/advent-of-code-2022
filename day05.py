import dataclasses
import typing
import itertools
import collections
import re

FILENAME = "day5_data.txt"


def yield_data(filename: str) -> typing.Iterator[str]:
    with open(file=filename, mode="r") as read_file:
        for line in read_file:
            yield line.rstrip()


def grouper(
    iterable: typing.Iterable, n: int, fillvalue=None
):  # from itertools recipes
    "Collect data into non-overlapping fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)


@dataclasses.dataclass
class RearrangementProcedure:
    qty: int
    from_stack: int
    to_stack: int


class CrateStacks(typing.DefaultDict[int, collections.deque]):
    def __init__(self):
        super().__init__(collections.deque)

    def move_crate(self, from_stack: int, to_stack: int) -> None:
        self[to_stack].append(self[from_stack].pop())

    def procedure_move(self, rearrangement_procedure: RearrangementProcedure) -> None:
        for _ in range(rearrangement_procedure.qty):
            self.move_crate(
                rearrangement_procedure.from_stack, rearrangement_procedure.to_stack
            )

    def procedure_move_multiple(
        self, rearrangement_procedure: RearrangementProcedure
    ) -> None:
        move_crates = collections.deque()
        for _ in range(rearrangement_procedure.qty):
            move_crates.append(self[rearrangement_procedure.from_stack].pop())
        for crate in reversed(move_crates):
            self[rearrangement_procedure.to_stack].append(crate)

    def crates_on_top_stacks(self) -> str:
        return "".join(self[stack_index][-1] for stack_index in range(1, len(self) + 1))


def yield_crates(line: str) -> typing.Iterator[str]:
    for group in grouper(line, 4):  # type: ignore
        group: tuple[str, str, str, typing.Optional[str]]
        yield group[1]


def create_crate_stacks(lines: typing.Iterator[str]) -> CrateStacks:
    crate_stacks = CrateStacks()
    for line in lines:
        if not "[" in line:
            break
        for index, string in enumerate(yield_crates(line), 1):
            if string == " ":
                continue
            crate_stacks[index].appendleft(string)

    _ = next(lines)
    return crate_stacks


def create_rearrangment_procedures(
    lines: typing.Iterator[str],
) -> typing.Iterator[RearrangementProcedure]:
    for line in lines:
        search = re.search("move (\\d+) from (\\d+) to (\\d+)", line)
        if search:
            yield RearrangementProcedure(*(int(value) for value in search.groups()))


def part1(filename: str) -> None:
    lines = yield_data(filename)
    crate_stacks = create_crate_stacks(lines)
    for rearrangement_procedure in create_rearrangment_procedures(lines):
        crate_stacks.procedure_move(rearrangement_procedure)
    print(crate_stacks.crates_on_top_stacks())


def part2(filename: str) -> None:
    lines = yield_data(filename)
    crate_stacks = create_crate_stacks(lines)
    for rearrangement_procedure in create_rearrangment_procedures(lines):
        crate_stacks.procedure_move_multiple(rearrangement_procedure)
    print(crate_stacks.crates_on_top_stacks())


def main():
    part1(FILENAME)
    part2(FILENAME)


if __name__ == "__main__":
    main()
