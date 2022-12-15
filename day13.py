import dataclasses
import itertools
import typing

FILENAME = "day13_data.txt"


def yield_lines(filename: str) -> typing.Iterator[str]:
    with open(file=filename, mode="r") as read_file:
        for line in read_file:
            yield line.rstrip()


def create_list_of_lists(line: str) -> list:
    list_of_lists = []
    open_brackets = 0
    inner_line = ""
    for character in line[1:-1]:
        if character == "," and not inner_line:
            continue
        elif character == "," and inner_line:
            inner_line = f"{inner_line}{character}"
        elif character == "[":
            open_brackets += 1
            inner_line = f"{inner_line}{character}"
        elif character == "]":
            open_brackets -= 1
            inner_line = f"{inner_line}{character}"
        elif inner_line:
            inner_line = f"{inner_line}{character}"
        else:
            list_of_lists.append(int(character))
        if inner_line and open_brackets == 0:
            list_of_lists.append(create_list_of_lists(inner_line))
            inner_line = ""
    return list_of_lists


@dataclasses.dataclass
class PacketPair:
    left: list
    right: list

    def is_right_order(self) -> bool:
        print(self)
        for left, right in itertools.zip_longest(
            self.left, self.right, fillvalue="Runout"
        ):
            print(left, right)
            if isinstance(left, int) and isinstance(right, int):
                if left < right:
                    return True
                elif left > right:
                    return False
            elif left == "Runout" and right != "Runout":
                return True
            elif right == "Runout" and left != "Runout":
                return False
            elif isinstance(left, list) and isinstance(right, list):
                packet_pair = PacketPair(left, right)
                if not packet_pair.is_right_order():
                    return False

            elif isinstance(left, int) and isinstance(right, list):
                packet_pair = PacketPair([left], right)
                if not packet_pair.is_right_order():
                    return False
            elif isinstance(left, list) and isinstance(right, int):
                packet_pair = PacketPair(left, [right])
                if not packet_pair.is_right_order():
                    return False

        return True


def create_packet_pairs(lines: typing.Iterator[str]) -> typing.Iterator[PacketPair]:
    while True:
        left = create_list_of_lists(next(lines))
        right = create_list_of_lists(next(lines))
        yield PacketPair(left, right)
        try:
            next(lines)
        except StopIteration:
            break


def part1(filename: str) -> None:
    lines = yield_lines(filename)
    right_order_pairs_index = []
    for index, packet_pair in enumerate(create_packet_pairs(lines), 1):
        # print(packet_pair)
        if packet_pair.is_right_order():
            right_order_pairs_index.append(index)
    print(sum(right_order_pairs_index))


def part2(filename: str) -> None:
    lines = yield_lines(filename)


def main():
    part1(TEST_FILENAME)
    # part2(TEST_FILENAME)


if __name__ == "__main__":
    main()
