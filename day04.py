import dataclasses
from typing import Iterator


FILENAME = "day4_data.txt"


def yield_data(filename: str) -> Iterator[str]:
    with open(file=filename, mode="r") as read_file:
        for line in read_file:
            yield line.strip()


@dataclasses.dataclass(frozen=True)
class IdPair:
    id_start: int
    id_end: int

    def fully_contains(self, other: "IdPair") -> bool:
        return self.id_start <= other.id_start and self.id_end >= other.id_end

    def overlaps_other(self, other: "IdPair") -> bool:
        return self.id_start <= other.id_end and self.id_end >= other.id_start


@dataclasses.dataclass(frozen=True)
class AssignmentIdPairs:
    first_id_pair: IdPair
    second_id_pair: IdPair

    def one_pair_fully_contains_other(self) -> bool:
        return self.first_id_pair.fully_contains(
            self.second_id_pair
        ) or self.second_id_pair.fully_contains(self.first_id_pair)

    def one_pair_overlaps_other(self) -> bool:
        return self.first_id_pair.overlaps_other(self.second_id_pair)


def create_assignment_pairs(lines: Iterator[str]) -> Iterator[AssignmentIdPairs]:
    for line in lines:
        first, second = line.split(",")
        first_id_pair = IdPair(*(int(id) for id in first.split("-")))
        second_id_pair = IdPair(*(int(id) for id in second.split("-")))
        yield AssignmentIdPairs(first_id_pair, second_id_pair)


def main():
    lines = yield_data(FILENAME)
    print(
        sum(
            assignemnt_pair.one_pair_fully_contains_other()
            for assignemnt_pair in create_assignment_pairs(lines)
        )
    )

    lines = yield_data(FILENAME)
    print(
        sum(
            assignemnt_pair.one_pair_overlaps_other()
            for assignemnt_pair in create_assignment_pairs(lines)
        )
    )


if __name__ == "__main__":
    main()
