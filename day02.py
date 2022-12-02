import dataclasses
import enum
from typing import Iterator

FILENAME = "day2_data.txt"


def yield_data(filename: str) -> Iterator[str]:
    with open(file=filename, mode="r") as read_file:
        for line in read_file:
            yield line.strip()


class Shape(enum.Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


shape_conversion = {
    "A": Shape.ROCK,
    "B": Shape.PAPER,
    "C": Shape.SCISSORS,
    "X": Shape.ROCK,
    "Y": Shape.PAPER,
    "Z": Shape.SCISSORS,
}


def strategy2_conversion(player1: str, player2: str) -> Shape:
    shape = shape_conversion[player1]
    if player2 == "X":
        for key, value in round_states.items():
            if key[0] == shape_conversion[player1] and value[1] == RoundOutcome.LOSS:
                shape = key[1]

    if player2 == "Z":
        for key, value in round_states.items():
            if key[0] == shape_conversion[player1] and value[1] == RoundOutcome.WIN:
                shape = key[1]
    return shape


class RoundOutcome(enum.IntEnum):
    LOSS = 0
    DRAW = 3
    WIN = 6


round_states: dict[tuple[Shape, Shape], tuple[RoundOutcome, RoundOutcome]] = {
    (Shape.ROCK, Shape.SCISSORS): (RoundOutcome.WIN, RoundOutcome.LOSS),
    (Shape.SCISSORS, Shape.PAPER): (RoundOutcome.WIN, RoundOutcome.LOSS),
    (Shape.PAPER, Shape.ROCK): (RoundOutcome.WIN, RoundOutcome.LOSS),
    (Shape.SCISSORS, Shape.ROCK): (RoundOutcome.LOSS, RoundOutcome.WIN),
    (Shape.PAPER, Shape.SCISSORS): (RoundOutcome.LOSS, RoundOutcome.WIN),
    (Shape.ROCK, Shape.PAPER): (RoundOutcome.LOSS, RoundOutcome.WIN),
}


@dataclasses.dataclass
class Round:
    choices: tuple[Shape, Shape]

    def score(self) -> tuple[int, int]:
        round_outcome = round_states.get(
            self.choices, (RoundOutcome.DRAW, RoundOutcome.DRAW)
        )
        return (
            self.choices[0].value + round_outcome[0],
            self.choices[1].value + round_outcome[1],
        )

    def player1_score(self) -> int:
        return self.score()[0]

    def player2_score(self) -> int:
        return self.score()[1]


def create_rounds(lines: Iterator[str], part1: bool = True) -> list[Round]:
    rounds: list[Round] = []
    for line in lines:
        line: str
        player1, player2 = line.split()
        player1_choice = shape_conversion[player1]
        if part1:
            player2_choice = shape_conversion[player2]
        else:
            player2_choice = strategy2_conversion(player1, player2)
        round = Round((player1_choice, player2_choice))
        rounds.append(round)

    return rounds


def main():
    data = yield_data(FILENAME)
    rounds = create_rounds(data, False)
    player2_score = sum(round.player2_score() for round in rounds)
    print(player2_score)


if __name__ == "__main__":
    main()
