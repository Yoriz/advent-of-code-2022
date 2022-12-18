import collections
import dataclasses
import typing

FILENAME = "year2022\day18_data.txt"


def yield_lines(filename: str) -> typing.Iterator[str]:
    with open(file=filename, mode="r") as read_file:
        for line in read_file:
            yield line.rstrip()


@dataclasses.dataclass(frozen=True)
class Coordinate:
    x: int
    y: int
    z: int

    def shifted_coordinate(self, x: int = 0, y: int = 0, z: int = 0) -> "Coordinate":
        return Coordinate(self.x + x, self.y + y, self.z + z)


@dataclasses.dataclass(frozen=True)
class CubeSize:
    x: int = 1
    y: int = 1
    z: int = 1


@dataclasses.dataclass(frozen=True)
class FaceCoordinate:
    start: Coordinate
    end: Coordinate

    def shifted_face_coordinate(
        self, x: int = 0, y: int = 0, z: int = 0
    ) -> "FaceCoordinate":
        start = self.start.shifted_coordinate(x, y, z)
        end = self.end.shifted_coordinate(x, y, z)
        return FaceCoordinate(start, end)


@dataclasses.dataclass(frozen=True)
class Cube:
    location: Coordinate
    size: CubeSize
    faces: set[FaceCoordinate] = dataclasses.field(default_factory=set)


def cube_face_coordinates(
    location: Coordinate, cube_size: CubeSize
) -> set[FaceCoordinate]:
    face_coordinate_x_y = FaceCoordinate(
        location, location.shifted_coordinate(x=cube_size.x, y=cube_size.y)
    )
    face_coordinate_x_y_z = face_coordinate_x_y.shifted_face_coordinate(z=cube_size.z)

    face_coordinate_y_z = FaceCoordinate(
        location, location.shifted_coordinate(y=cube_size.y, z=cube_size.z)
    )
    face_coordinate_y_z_x = face_coordinate_y_z.shifted_face_coordinate(x=cube_size.x)

    face_coordinate_z_x = FaceCoordinate(
        location, location.shifted_coordinate(z=cube_size.z, x=cube_size.x)
    )
    face_coordinate_z_x_y = face_coordinate_z_x.shifted_face_coordinate(y=cube_size.y)
    return {
        face_coordinate_x_y,
        face_coordinate_x_y_z,
        face_coordinate_y_z,
        face_coordinate_y_z_x,
        face_coordinate_z_x,
        face_coordinate_z_x_y,
    }


def create_cubes(lines: typing.Iterator[str]) -> typing.Iterator[Cube]:
    for line in lines:
        x, y, z = line.split(",")
        coordinate = Coordinate(int(x), int(y), int(z))
        cube_size = CubeSize()
        face_coordinates = cube_face_coordinates(coordinate, cube_size)
        yield Cube(coordinate, cube_size, face_coordinates)


def part1(filename: str) -> None:
    lines = yield_lines(filename)
    cube_faces = collections.Counter()
    for cube in create_cubes(lines):
        cube_faces.update(cube.faces)
    unique_faces = [key for key, value in cube_faces.items() if value == 1]
    print(len(unique_faces))


def part2(filename: str) -> None:
    lines = yield_lines(filename)


def main():
    part1(FILENAME)
    # part2(FILENAME)


if __name__ == "__main__":
    main()
