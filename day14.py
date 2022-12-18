import dataclasses
import enum
import itertools
import typing

FILENAME = "day14_data.txt"


def yield_lines(filename: str) -> typing.Iterator[str]:
    with open(file=filename, mode="r") as read_file:
        for line in read_file:
            yield line.rstrip()


class LocationType(enum.Enum):
    AIR = "."
    ROCK = "#"
    SAND_FALLING = "o"
    SAND_AT_REST = "O"
    SAND_ENTRANCE = "+"
    VOID = "~"


@dataclasses.dataclass(frozen=True)
class Location:
    x: int = 0
    y: int = 0
    type: typing.Optional[LocationType] = None

    def neighbour_location(self, location_direction: "LocationDirection") -> "Location":
        other_location: "Location" = location_direction.value
        return Location(self.x + other_location.x, self.y + other_location.y)


@enum.unique
class LocationDirection(enum.Enum):
    DOWN = Location(0, 1)
    DOWN_LEFT = Location(-1, 1)
    DOWN_RIGHT = Location(1, 1)


@dataclasses.dataclass
class Grid:
    start_location: Location
    end_location: Location
    location_type: LocationType
    contained_grids: list["Grid"] = dataclasses.field(default_factory=list)
    individual_locations: list[Location] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        start_location = self.start_location
        end_location = self.end_location
        self.start_location = Location(
            min(start_location.x, end_location.x), min(start_location.y, end_location.y)
        )
        self.end_location = Location(
            max(start_location.x, end_location.x), max(start_location.y, end_location.y)
        )

    def has_location(self, location: Location) -> bool:
        return all(
            (
                location.x > self.start_location.x - 1,
                location.x < self.end_location.x + 1,
                location.y > self.start_location.y - 1,
                location.y < self.end_location.y + 1,
            )
        )

    def resize_to_contain_location(self, location: Location) -> None:
        if not (location.x > self.start_location.x - 1):
            self.start_location = dataclasses.replace(self.start_location, x=location.x)
        if not (location.x < self.end_location.x + 1):
            self.end_location = dataclasses.replace(self.end_location, x=location.x)
        if not (location.y > self.start_location.y - 1):
            self.start_location = dataclasses.replace(self.start_location, y=location.y)
        if not (location.y < self.end_location.y + 1):
            self.end_location = dataclasses.replace(self.end_location, y=location.y)

    def grids_location(self, location: Location) -> Location:
        contained_location = Location(location.x, location.y, LocationType.VOID)
        if not self.has_location(location):
            return contained_location
        else:
            contained_location = dataclasses.replace(
                contained_location, type=self.location_type
            )

        for contained_grid in self.contained_grids:
            if contained_grid.has_location(location):
                contained_location = dataclasses.replace(
                    contained_location, type=contained_grid.location_type
                )
        for individual_location in self.individual_locations:
            if (
                location.x == individual_location.x
                and location.y == individual_location.y
            ):
                contained_location = individual_location

        return contained_location

    def add_contained_grid(self, grid: "Grid", resize_grid: bool = True) -> None:
        if resize_grid:
            for location in (grid.start_location, grid.end_location):
                self.resize_to_contain_location(location)
        self.contained_grids.append(grid)

    def add_individual_location(
        self, location: Location, resize_grid: bool = False
    ) -> None:
        if resize_grid:
            self.resize_to_contain_location(location)
        self.individual_locations.append(location)

    def display_str(
        self,
        display_start_location: typing.Optional[Location] = None,
        display_end_location: typing.Optional[Location] = None,
    ) -> str:
        start_location = display_start_location or self.start_location
        end_location = display_end_location or self.end_location
        rows: list[str] = []
        for y_index in range(start_location.y, end_location.y + 1):
            row: list[str] = []
            for x_index in range(start_location.x, end_location.x + 1):
                location = self.grids_location(Location(x_index, y_index))
                if location.type:
                    row.append(location.type.value)
            rows.append("".join(row))
        return "\n".join(rows)


@dataclasses.dataclass
class InfinateXGrid(Grid):
    def has_location(self, location: Location) -> bool:
        return all(
            (
                True,
                True,
                location.y > self.start_location.y - 1,
                location.y < self.end_location.y + 1,
            )
        )


def create_rock_grids(lines: typing.Iterator[str]) -> typing.Iterator[Grid]:
    for line in lines:
        locations_strings = line.split(" -> ")
        locations = []
        for location_string in locations_strings:
            x, y = location_string.split(",")
            locations.append(Location(int(x), int(y)))

        for start_location, end_location in itertools.pairwise(locations):
            yield Grid(start_location, end_location, LocationType.ROCK)


def add_unit_of_sand(cave_grid: Grid) -> Location:
    sand_location = Location(500, 0, LocationType.SAND_FALLING)
    cave_location = Location()
    while True:
        for location_direction in LocationDirection:
            neighbour_location = sand_location.neighbour_location(location_direction)
            cave_location = cave_grid.grids_location(neighbour_location)
            if cave_location.type in (LocationType.AIR, LocationType.VOID):
                sand_location = dataclasses.replace(
                    sand_location, x=neighbour_location.x, y=neighbour_location.y
                )
                break
        if cave_location.type in (LocationType.ROCK, LocationType.SAND_AT_REST):
            sand_resting_location = dataclasses.replace(
                sand_location, type=LocationType.SAND_AT_REST
            )
            cave_grid.add_individual_location(sand_resting_location)
            return sand_resting_location
        elif cave_location.type == LocationType.VOID:
            sand_resting_location = dataclasses.replace(
                sand_location, type=LocationType.VOID
            )
            return sand_resting_location


def part1(filename: str) -> None:
    lines = yield_lines(filename)
    rock_grids = create_rock_grids(lines)

    sand_entrance_location = Location(500, 0, LocationType.SAND_ENTRANCE)
    cave_grid = Grid(sand_entrance_location, sand_entrance_location, LocationType.AIR)
    cave_grid.add_individual_location(sand_entrance_location, True)
    for rock_grid in rock_grids:
        cave_grid.add_contained_grid(rock_grid)
    count = 0
    for count in itertools.count():
        print(count)
        location = add_unit_of_sand(cave_grid)
        if location.type == LocationType.VOID:
            break

    # print(cave_grid.display_str())
    print(f"Units of sand: {count}")


def part2(filename: str) -> None:
    lines = yield_lines(filename)
    rock_grids = create_rock_grids(lines)

    sand_entrance_location = Location(500, 0, LocationType.SAND_ENTRANCE)
    cave_grid = InfinateXGrid(
        sand_entrance_location, sand_entrance_location, LocationType.AIR
    )
    cave_grid.add_individual_location(sand_entrance_location, True)
    for rock_grid in rock_grids:
        cave_grid.add_contained_grid(rock_grid)
    max_y_location = cave_grid.end_location.y
    max_y_location += 2
    cave_grid.end_location = Location(cave_grid.end_location.x, max_y_location)
    infiate_x_grid = InfinateXGrid(
        Location(0, max_y_location), Location(0, max_y_location), LocationType.ROCK
    )
    cave_grid.add_contained_grid(infiate_x_grid, False)
    count = 0
    for count in itertools.count(1):
        print(count)
        location = add_unit_of_sand(cave_grid)
        if location.x == 500 and location.y == 0:
            break

    # print(cave_grid.display_str(Location(488, 0), Location(512, 12)))
    print(f"Units of sand: {count}")


def main():
    part1(FILENAME)
    part2(FILENAME)


if __name__ == "__main__":
    main()
