import dataclasses
import enum
import operator
import typing

FILENAME = "day15_data.txt"


def yield_lines(filename: str) -> typing.Iterator[str]:
    with open(file=filename, mode="r") as read_file:
        for line in read_file:
            yield line.rstrip()


@enum.unique
class LocationMark(enum.Enum):
    SENSOR = "S"
    BEACON = "B"
    NOT_BEACON = "#"
    EMPTY = "."


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

    def shifted_location(self, other: "Location") -> "Location":
        return Location(self.x + other.x, self.y + other.y)


@enum.unique
class LocationDirection(enum.Enum):
    UP = Location(0, -1)
    RIGHT = Location(1, 0)
    DOWN = Location(0, 1)
    LEFT = Location(-1, 0)


@dataclasses.dataclass(frozen=True)
class RowCoverage:
    x_start: int
    x_end: int

    def overlaps(self, other: "RowCoverage") -> bool:
        return self.x_start <= other.x_end and self.x_end >= other.x_start

    def merge(self, other: "RowCoverage") -> "RowCoverage":
        return RowCoverage(
            min(self.x_start, other.x_start), max(self.x_end, other.x_end)
        )

    @property
    def count(self) -> int:
        return (self.x_end + 1) - self.x_start


@dataclasses.dataclass
class Sensor:
    location: Location
    closest_beacon_location: Location

    @property
    def distance_to_closest_beacon(self) -> int:
        return self.location.distance(self.closest_beacon_location)

    @property
    def coverage_min_x(self) -> Location:
        location = Location(-self.distance_to_closest_beacon, 0)
        return self.location.shifted_location(location)

    @property
    def coverage_max_x(self) -> Location:
        location = Location(self.distance_to_closest_beacon, 0)
        return self.location.shifted_location(location)

    @property
    def coverage_min_y(self) -> Location:
        location = Location(0, -self.distance_to_closest_beacon)
        return self.location.shifted_location(location)

    @property
    def coverage_max_y(self) -> Location:
        location = Location(0, self.distance_to_closest_beacon)
        return self.location.shifted_location(location)

    def location_mark(self, location: Location) -> LocationMark:
        location_mark = LocationMark.EMPTY
        if self.location == location:
            location_mark = LocationMark.SENSOR
        elif self.closest_beacon_location == location:
            location_mark = LocationMark.BEACON
        elif self.location.distance(location) <= self.distance_to_closest_beacon:
            location_mark = LocationMark.NOT_BEACON

        return location_mark

    def non_beacon_row_coverage(self, y: int) -> typing.Optional[RowCoverage]:
        row_coverage: typing.Optional[RowCoverage] = None
        y_distance = abs(self.location.y - y)
        if y_distance < self.distance_to_closest_beacon:
            x_length = self.distance_to_closest_beacon - y_distance
            row_coverage = RowCoverage(
                self.location.x - x_length, self.location.x + x_length
            )
        if y_distance == self.distance_to_closest_beacon:
            row_coverage = RowCoverage(self.location.x, self.location.x)

        return row_coverage


def create_sensor(line: str) -> Sensor:
    sensor_text, beacon_text = line.split(":")
    sensor_x_text, sensor_y_text = sensor_text.split(",")
    sensor_x = sensor_x_text.split("=")[1]
    sensor_y = sensor_y_text.split("=")[1]
    beacon_x_text, becaon_y_text = beacon_text.split(",")
    beacon_x = beacon_x_text.split("=")[1]
    beacon_y = becaon_y_text.split("=")[1]
    sensor_location = Location(int(sensor_x), int(sensor_y))
    beacon_location = Location(int(beacon_x), int(beacon_y))
    return Sensor(sensor_location, beacon_location)


def part1(filename: str) -> None:
    lines = yield_lines(filename)
    sensors: list[Sensor] = []
    row_coverages: list[RowCoverage] = []
    y_row = 2000000
    beacons_in_row: set[int] = set()
    for line in lines:
        sensor = create_sensor(line)
        sensors.append(sensor)
        row_coverage = sensor.non_beacon_row_coverage(y_row)
        if row_coverage:
            row_coverages.append(row_coverage)
        if sensor.closest_beacon_location.y == y_row:
            beacons_in_row.add(sensor.closest_beacon_location.x)
    row_coverages.sort(key=operator.attrgetter("x_start"))
    merged_row_coverages: list[RowCoverage] = []
    current_row_coverage = row_coverages[0]
    for row_coverage in row_coverages[1:]:
        if current_row_coverage.overlaps(row_coverage):
            current_row_coverage = current_row_coverage.merge(row_coverage)
        else:
            merged_row_coverages.append(current_row_coverage)
            current_row_coverage = row_coverage
    merged_row_coverages.append(current_row_coverage)
    non_beacon_count = sum(row_coverage.count for row_coverage in merged_row_coverages)
    beacon_count = len(beacons_in_row)
    print(non_beacon_count - beacon_count)


def part2(filename: str) -> None:
    lines = yield_lines(filename)
    sensors: list[Sensor] = []

    y_rows = 4000000
    for line in lines:
        sensor = create_sensor(line)
        sensors.append(sensor)

    for y_row in range(0, y_rows + 1):
        row_coverages: list[RowCoverage] = []
        for sensor in sensors:
            row_coverage = sensor.non_beacon_row_coverage(y_row)
            if row_coverage:
                row_coverages.append(row_coverage)

        row_coverages.sort(key=operator.attrgetter("x_start"))
        merged_row_coverages: list[RowCoverage] = []
        current_row_coverage = row_coverages[0]
        for row_coverage in row_coverages[1:]:
            if current_row_coverage.overlaps(row_coverage):
                current_row_coverage = current_row_coverage.merge(row_coverage)
            else:
                merged_row_coverages.append(current_row_coverage)
                current_row_coverage = row_coverage
        merged_row_coverages.append(current_row_coverage)
        if len(merged_row_coverages) > 1:
            print(y_row, merged_row_coverages)

    # found 3249595 [RowCoverage(x_start=-933677, x_end=3340223), RowCoverage(x_start=3340225, x_end=4217259)]
    x = 3340224
    y = 3249595
    print((x * 4000000) + y)


def main():
    part1(FILENAME)
    part2(FILENAME)


if __name__ == "__main__":
    main()
