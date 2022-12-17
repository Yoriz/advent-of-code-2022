import collections
import dataclasses
import enum
import typing

TEST_FILENAME = (
    r"C:\Users\Dave\Documents\VsWorkspace\advent_of_code\year2022\day12_testdata.txt"
)
FILENAME = r"C:\Users\Dave\Documents\VsWorkspace\advent_of_code\year2022\day12_data.txt"


def yield_lines(filename: str) -> typing.Iterator[str]:
    with open(file=filename, mode="r") as read_file:
        for line in read_file:
            yield line.rstrip()


Grid = list[list[str]]


def create_grid(lines: typing.Iterator[str]) -> Grid:
    return [list(line) for line in lines]


@dataclasses.dataclass(frozen=True)
class Location:
    x: int = 0
    y: int = 0

    def neighbour_location(self, location_direction: "LocationDirection") -> "Location":
        other_location: "Location" = location_direction.value
        return Location(self.x + other_location.x, self.y + other_location.y)

    def relationship(self, other: "Location") -> "Location":
        return Location(other.x - self.x, other.y - self.y)

    def distance(self, other: "Location") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)


@enum.unique
class LocationDirection(enum.Enum):
    UP = Location(0, -1)
    RIGHT = Location(1, 0)
    DOWN = Location(0, 1)
    LEFT = Location(-1, 0)


@enum.unique
class LocationMark(enum.Enum):
    S = "S"
    E = "E"


def elevation_score(elevation: str) -> int:
    if elevation == LocationMark.S.value:
        elevation = "a"
    elif elevation == LocationMark.E.value:
        elevation = "z"
    return ord(elevation) - ord("a")


@dataclasses.dataclass
class HeightMap:
    grid: Grid
    start_location: Location
    end_location: Location

    def is_location_in_grid(self, location: Location) -> bool:
        return all(
            (
                location.x > -1,
                location.x < self.max_x_location + 1,
                location.y > -1,
                location.y < self.max_y_location + 1,
            )
        )

    def available_location_directions(
        self, location: Location
    ) -> list[LocationDirection]:
        location_directions: list[LocationDirection] = []
        for location_direction in LocationDirection:
            neighbour_location = location.neighbour_location(location_direction)
            if self.is_location_in_grid(neighbour_location):
                location_directions.append(location_direction)
        return location_directions

    def grid_location_letter(self, location: Location) -> str:
        return self.grid[location.y][location.x]

    def grid_location_elevation_score(self, location: Location) -> int:
        location_letter = self.grid_location_letter(location)
        return elevation_score(location_letter)

    def letter_locations(self, letter: str) -> list[Location]:
        locations: list[Location] = []
        for y_index, row in enumerate(self.grid):
            for x_index, elevation in enumerate(row):
                if elevation != letter:
                    continue
                locations.append(Location(x_index, y_index))
        return locations

    @property
    def max_x_location(self) -> int:
        return len(self.grid[0]) - 1

    @property
    def max_y_location(self) -> int:
        return len(self.grid) - 1

    @property
    def total_grid_locations(self) -> int:
        return len(self.grid) * len(self.grid[0])


def create_heightmap(lines: typing.Iterator[str]) -> HeightMap:
    grid = create_grid(lines)
    start_location = Location()
    end_location = Location()
    for y_index, row in enumerate(grid):
        for x_index, elevation in enumerate(row):
            if elevation == LocationMark.S.value:
                start_location = Location(x_index, y_index)
            elif elevation == LocationMark.E.value:
                end_location = Location(x_index, y_index)

    return HeightMap(grid, start_location, end_location)


def construct_shortest_path(
    current_location: Location,
    start_location: Location,
    predecessor: dict[Location, Location],
):
    path = []
    while current_location != start_location:
        path.append(current_location)
        current_location = predecessor[current_location]
    path.append(start_location)
    return path[::-1]


def find_shortest_path(
    height_map: HeightMap, start_location: Location
) -> typing.Optional[list[Location]]:
    visited_locations: set[Location] = set()
    deque = collections.deque((start_location,))
    predecessor: dict[Location, Location] = {}
    while deque:
        current_location = deque.popleft()
        if current_location == height_map.end_location:
            return construct_shortest_path(
                current_location, start_location, predecessor
            )

        if current_location in visited_locations:
            continue

        visited_locations.add(current_location)

        for location_direction in height_map.available_location_directions(
            current_location
        ):
            neighbour_location = current_location.neighbour_location(location_direction)
            if neighbour_location in visited_locations:
                continue

            if (
                height_map.grid_location_elevation_score(neighbour_location)
                - height_map.grid_location_elevation_score(current_location)
                > 1
            ):
                continue
            deque.append(neighbour_location)
            predecessor[neighbour_location] = current_location

    return None


def part1(filename: str) -> None:
    lines = yield_lines(filename)
    heightmap = create_heightmap(lines)
    shortest_path = find_shortest_path(heightmap, heightmap.start_location)
    if shortest_path:
        print(len(shortest_path) - 1)


def part2(filename: str) -> None:
    lines = yield_lines(filename)
    heightmap = create_heightmap(lines)
    start_locations = heightmap.letter_locations("a")
    start_locations.extend((heightmap.start_location,))
    shortest_paths: list[int] = []
    for start_location in start_locations:
        shortest_path = find_shortest_path(heightmap, start_location)
        if shortest_path:
            shortest_paths.append(len(shortest_path) - 1)
    print(min(shortest_paths))


def main():
    part1(FILENAME)
    part2(FILENAME)


if __name__ == "__main__":
    main()
