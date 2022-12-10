import dataclasses
import enum
import typing

FILENAME = "day9_data.txt"


def yield_lines(filename: str) -> typing.Iterator[str]:
    with open(file=filename, mode="r") as read_file:
        for line in read_file:
            yield line.rstrip()


@dataclasses.dataclass(frozen=True)
class Location:
    x: int = 0
    y: int = 0

    def neighbour_location(self, location_direction: "LocationDirection") -> "Location":
        other_location: "Location" = location_direction.value
        return Location(self.x + other_location.x, self.y + other_location.y)

    def relationship(self, other: "Location") -> "Location":
        return Location(other.x - self.x, other.y - self.y)


@enum.unique
class LocationDirection(enum.Enum):
    UP = Location(0, 1)
    UP_RIGHT = Location(1, 1)
    RIGHT = Location(1, 0)
    DOWN_RIGHT = Location(1, -1)
    DOWN = Location(0, -1)
    DOWN_LEFT = Location(-1, -1)
    LEFT = Location(-1, 0)
    UP_LEFT = Location(-1, 1)


location_direction_dict = {
    "U": LocationDirection.UP,
    "R": LocationDirection.RIGHT,
    "D": LocationDirection.DOWN,
    "L": LocationDirection.LEFT,
}

tail_movement_dict = {
    Location(0, -2): LocationDirection.UP,
    Location(x=-1, y=-2): LocationDirection.UP_RIGHT,
    Location(x=-2, y=-2): LocationDirection.UP_RIGHT,
    Location(x=-2, y=-1): LocationDirection.UP_RIGHT,
    Location(x=-2, y=0): LocationDirection.RIGHT,
    Location(x=-2, y=1): LocationDirection.DOWN_RIGHT,
    Location(x=-2, y=2): LocationDirection.DOWN_RIGHT,
    Location(x=-1, y=2): LocationDirection.DOWN_RIGHT,
    Location(0, 2): LocationDirection.DOWN,
    Location(x=1, y=2): LocationDirection.DOWN_LEFT,
    Location(x=2, y=2): LocationDirection.DOWN_LEFT,
    Location(x=2, y=1): LocationDirection.DOWN_LEFT,
    Location(x=2, y=0): LocationDirection.LEFT,
    Location(x=2, y=-1): LocationDirection.UP_LEFT,
    Location(x=2, y=-2): LocationDirection.UP_LEFT,
    Location(x=1, y=-2): LocationDirection.UP_LEFT,
}


def create_location_directions(
    lines: typing.Iterator[str],
) -> typing.Iterator[LocationDirection]:
    for line in lines:
        motion, amount = line.split(" ")
        for _ in range(int(amount)):
            yield location_direction_dict[motion]


@dataclasses.dataclass
class Rope:
    knot_qty: dataclasses.InitVar[int] = 2
    tail_visited_locations: set[Location] = dataclasses.field(
        default_factory=set, init=False
    )
    knots: list[Location] = dataclasses.field(default_factory=list, init=False)

    def __post_init__(self, knot_qty):
        for _ in range(knot_qty):
            self.knots.append(Location())

        self.update_tail_visited_location()

    def update_tail_visited_location(self):
        self.tail_visited_locations.add(self.knots[-1])

    def move_head_knot(self, location_direction: LocationDirection) -> None:
        self.knots[0] = self.knots[0].neighbour_location(location_direction)
        self.update_knot_locations()

    def update_knot_locations(self) -> None:

        for index, _ in enumerate(self.knots[:-1]):
            knot_relationship = self.knots[index].relationship(self.knots[index + 1])
            location_direction = tail_movement_dict.get(knot_relationship)
            if location_direction:
                self.knots[index + 1] = self.knots[index + 1].neighbour_location(
                    location_direction
                )

        self.update_tail_visited_location()

    def qty_positions_tail_visited(self) -> int:
        return len(self.tail_visited_locations)


def part1(filename: str) -> None:
    lines = yield_lines(filename)
    location_directions = create_location_directions(lines)
    rope = Rope()
    for index, location_direction in enumerate(location_directions):
        rope.move_head_knot(location_direction)
    print(rope.qty_positions_tail_visited())


def part2(filename: str) -> None:
    lines = yield_lines(filename)
    location_directions = create_location_directions(lines)
    rope = Rope(10)
    for index, location_direction in enumerate(location_directions):
        rope.move_head_knot(location_direction)
    print(rope.qty_positions_tail_visited())


def main():
    part1(FILENAME)
    part2(FILENAME)


if __name__ == "__main__":
    main()
