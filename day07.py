import dataclasses
import typing

FILENAME = "day7_data.txt"


def yield_data(filename: str) -> typing.Iterator[str]:
    with open(file=filename, mode="r") as read_file:
        for line in read_file:
            yield line.rstrip()


@dataclasses.dataclass
class File:
    name: str
    size: int


@dataclasses.dataclass
class Directory:
    name: str
    parent_directory: typing.Optional["Directory"] = None
    directories: list["Directory"] = dataclasses.field(default_factory=list)
    files: list[File] = dataclasses.field(default_factory=list)

    def add_directory(self, directory: "Directory") -> None:
        directory.parent_directory = self
        self.directories.append(directory)

    def add_file(self, file: File) -> None:
        self.files.append(file)

    def get_directory(self, name: str) -> typing.Optional["Directory"]:
        for directory in self.directories:
            if directory.name == name:
                return directory
        return None

    def total_files_size(self) -> int:
        return sum(file.size for file in self.files)

    def total_size(self) -> int:
        total = self.total_files_size()
        for directory in self.directories:
            total += directory.total_size()
        return total


def create_root_directory() -> Directory:
    return Directory("/")


@dataclasses.dataclass
class FileSystem:
    directory: Directory = dataclasses.field(default_factory=create_root_directory)

    def change_directory(self, command: str, create_if_not_exist: bool = True) -> None:
        if command == "/":
            while True:
                if not self.directory.parent_directory:
                    break
                self.directory = self.directory.parent_directory
        elif command == "..":
            if not self.directory.parent_directory:
                return
            self.directory = self.directory.parent_directory
        else:
            directory = self.directory.get_directory(command)
            if directory:
                self.directory = directory
            elif not directory and create_if_not_exist:
                print(f"In Change Directory, directory added: {command}")
                directory = Directory(command)
                self.add_directory(directory)
                self.directory = directory
            else:
                print(f"No directoy named {command}")

    def add_directory(self, directory: Directory) -> None:
        self.directory.add_directory(directory)

    def directory_total_files_size(self) -> int:
        return self.directory.total_files_size()

    def directory_total_size(self) -> int:
        return self.directory.total_size()


def parse_list_line(
    line: str, file_system: FileSystem, ls_directory: Directory
) -> None:
    if line.startswith("dir"):
        _, directory_name = line.split(" ")
        print(f"List add directory: {directory_name} added to {ls_directory.name}")
        directory = Directory(directory_name)
        file_system.add_directory(directory)
        return None

    file_size, file_name = line.split(" ")
    print(f"List add file: {file_name}, {file_size} to {ls_directory.name}")
    file = File(file_name, int(file_size))
    ls_directory.add_file(file)
    return None


def parse_terminal_output(
    terminal_output: typing.Iterator[str], file_system: FileSystem
):
    ls_directory = None
    for line in terminal_output:
        if line.startswith("$ cd"):
            _, _, command = line.split(" ")
            print(f"Change Directory: {command}")
            file_system.change_directory(command)
            ls_directory = None
        elif line.startswith("$ ls"):
            ls_directory = file_system.directory
        elif ls_directory:
            parse_list_line(line, file_system, ls_directory)


def walk_directories(directory: Directory):
    yield directory
    for child_directory in directory.directories:
        yield from walk_directories(child_directory)


def part1(filename: str) -> None:
    lines = yield_data(filename)
    file_system = FileSystem()
    parse_terminal_output(lines, file_system)
    file_system.change_directory("/")
    total_sizes = 0
    for directory in walk_directories(file_system.directory):
        directory_total_size = directory.total_size()
        print(f"Dir: {directory.name}, Size: {directory_total_size}")
        if directory_total_size < 100000:
            total_sizes += directory_total_size
    print(total_sizes)


def part2(filename: str) -> None:
    lines = yield_data(filename)
    file_system = FileSystem()
    parse_terminal_output(lines, file_system)
    file_system.change_directory("/")
    outermost_size = file_system.directory_total_size()
    TOTAL_DISK_SPACE = 70000000
    REQUIRED_UNUSED_SPACE = 30000000
    unused_space = TOTAL_DISK_SPACE - outermost_size
    required_extra_unused_space = REQUIRED_UNUSED_SPACE - unused_space
    smallest_directory = file_system.directory
    for directory in walk_directories(file_system.directory):
        directory_total_size = directory.total_size()
        if directory_total_size < required_extra_unused_space:
            continue
        if directory_total_size < smallest_directory.total_size():
            smallest_directory = directory

    print(f"Dir: {smallest_directory.name}, Size: {smallest_directory.total_size()}")


def main():
    part1(FILENAME)
    part2(FILENAME)


if __name__ == "__main__":
    main()
