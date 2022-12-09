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

    def neightbour_location(
        self, location_direction: "LocationDirection"
    ) -> "Location":
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
    Location(x=-2, y=-1): LocationDirection.UP_RIGHT,
    Location(x=-2, y=0): LocationDirection.RIGHT,
    Location(x=-2, y=1): LocationDirection.DOWN_RIGHT,
    Location(x=-1, y=2): LocationDirection.DOWN_RIGHT,
    Location(0, 2): LocationDirection.DOWN,
    Location(x=1, y=2): LocationDirection.DOWN_LEFT,
    Location(x=2, y=1): LocationDirection.DOWN_LEFT,
    Location(x=2, y=0): LocationDirection.LEFT,
    Location(x=2, y=-1): LocationDirection.UP_LEFT,
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
    head: Location = Location()
    tail: Location = Location()
    tail_visited_locations: set[Location] = dataclasses.field(default_factory=set)

    def __post_init__(self):
        self.add_tail_visited_location()

    def add_tail_visited_location(self):
        self.tail_visited_locations.add(self.tail)

    def move_head_location(self, location_direction: LocationDirection) -> None:
        self.head = self.head.neightbour_location(location_direction)
        self.update_tail_location()

    def move_tail_location(self, location_direction: LocationDirection) -> None:
        self.tail = self.tail.neightbour_location(location_direction)
        self.add_tail_visited_location()

    def tail_relationship_location(self) -> Location:
        return self.head.relationship(self.tail)

    def update_tail_location(self) -> None:
        tail_relationship = self.tail_relationship_location()
        location_direction = tail_movement_dict.get(self.tail_relationship_location())
        if location_direction:
            self.move_tail_location(location_direction)

    def qty_positions_tail_visited(self) -> int:
        return len(self.tail_visited_locations)


def part1(filename: str) -> None:
    lines = yield_lines(filename)
    location_directions = create_location_directions(lines)
    rope = Rope()
    for index, location_direction in enumerate(location_directions):
        # if index == 2:
        #     break
        # print(location_direction)
        rope.move_head_location(location_direction)
    print(rope.qty_positions_tail_visited())
    # print(rope)


def part2(filename: str) -> None:
    lines = yield_lines(filename)
    # Part2 not yet done


def main():
    part1(FILENAME)
    # part2(FILENAME)


if __name__ == "__main__":
    main()
