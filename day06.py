import collections
import itertools
import typing

FILENAME = "day6_data.txt"


def yield_data(filename: str) -> typing.Iterator[str]:
    with open(file=filename, mode="r") as read_file:
        for line in read_file:
            yield line.rstrip()


def sliding_window(iterable: typing.Iterable, n: int):  # from itertools recipes
    # sliding_window('ABCDEFG', 4) -> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = collections.deque(itertools.islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)


def part1(filename: str) -> None:
    lines = yield_data(filename)
    line = next(lines)
    for index, item in enumerate(sliding_window(line, 4), 4):
        if len(set(item)) == 4:
            print(index)
            break


def part2(filename: str) -> None:
    lines = yield_data(filename)
    line = next(lines)
    for index, item in enumerate(sliding_window(line, 14), 14):
        if len(set(item)) == 14:
            print(index)
            break


def main():
    part1(FILENAME)
    part2(FILENAME)


if __name__ == "__main__":
    main()
