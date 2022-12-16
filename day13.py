import dataclasses
import enum
import functools
import itertools
import operator
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
    number = ""
    for character in line[1:-1]:
        if character == "," and not inner_line:
            if number:
                list_of_lists.append(int(number))
            number = ""
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
            number = f"{number}{character}"

        if inner_line and open_brackets == 0:
            list_of_lists.append(create_list_of_lists(inner_line))
            inner_line = ""
    if number:
        list_of_lists.append(int(number))
    return list_of_lists


class PacketOrderState(enum.IntEnum):
    RIGHT = -1
    UNDECIDED = 0
    WRONG = 1


@dataclasses.dataclass
class PacketPair:
    left: list
    right: list

    def is_right_order(self) -> PacketOrderState:
        for left, right in itertools.zip_longest(
            self.left, self.right, fillvalue="Runout"
        ):
            if isinstance(left, int) and isinstance(right, int):
                if left < right:
                    return PacketOrderState.RIGHT
                elif left > right:
                    return PacketOrderState.WRONG
                elif left == right:
                    continue
            elif left == "Runout":
                return PacketOrderState.RIGHT
            elif right == "Runout":
                return PacketOrderState.WRONG

            elif isinstance(left, list) and isinstance(right, list):
                if not left and not right:
                    continue
                packet_pair = PacketPair(left, right)
                packet_order_state = packet_pair.is_right_order()
                if packet_order_state == PacketOrderState.UNDECIDED:
                    continue
                return packet_order_state

            elif isinstance(left, int) and isinstance(right, list):
                packet_pair = PacketPair([left], right)
                packet_order_state = packet_pair.is_right_order()
                if packet_order_state == PacketOrderState.UNDECIDED:
                    continue
                return packet_order_state

            elif isinstance(left, list) and isinstance(right, int):
                packet_pair = PacketPair(left, [right])
                packet_order_state = packet_pair.is_right_order()
                if packet_order_state == PacketOrderState.UNDECIDED:
                    continue
                return packet_order_state

        return PacketOrderState.UNDECIDED


def create_packet_pairs(lines: typing.Iterator[str]) -> typing.Iterator[PacketPair]:
    while True:
        left = create_list_of_lists(next(lines))
        right = create_list_of_lists(next(lines))
        yield PacketPair(left, right)
        try:
            next(lines)
        except StopIteration:
            break


def parse_list_of_lists(lines: typing.Iterator[str]) -> typing.Iterator[list]:
    while True:
        yield create_list_of_lists(next(lines))
        yield create_list_of_lists(next(lines))
        try:
            next(lines)
        except StopIteration:
            break


def compare_list_of_lists(left: list, right: list) -> int:
    packet_pair = PacketPair(left, right)
    return packet_pair.is_right_order()


def part1(filename: str) -> None:
    lines = yield_lines(filename)
    right_order_pairs_index = []
    for index, packet_pair in enumerate(create_packet_pairs(lines), 1):
        if packet_pair.is_right_order() == PacketOrderState.RIGHT:
            right_order_pairs_index.append(index)
    print(sum(right_order_pairs_index))


def part2(filename: str) -> None:
    lines = yield_lines(filename)
    list_of_lists = list(parse_list_of_lists(lines))
    divider_packets = [[[2]], [[6]]]
    list_of_lists.extend(divider_packets)
    list_of_lists.sort(key=functools.cmp_to_key(compare_list_of_lists))
    decoder_key_indexs = []
    for index, item in enumerate(list_of_lists, 1):
        if item in divider_packets:
            decoder_key_indexs.append(index)
    print(operator.mul(*decoder_key_indexs))


def main():
    part1(FILENAME)
    part2(FILENAME)


if __name__ == "__main__":
    main()
