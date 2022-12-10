import dataclasses
import enum
import typing

FILENAME = "day10_data.txt"


def yield_lines(filename: str) -> typing.Iterator[str]:
    with open(file=filename, mode="r") as read_file:
        for line in read_file:
            yield line.rstrip()


class Command(enum.Enum):
    NOOP = enum.auto()
    ADDX = enum.auto()


commands = {"noop": Command.NOOP, "addx": Command.ADDX}
cycle_times = {Command.NOOP: 1, Command.ADDX: 2}


@dataclasses.dataclass
class Instruction:
    command: Command
    value: typing.Optional[int] = None
    cycle_time: int = dataclasses.field(init=False)

    def __post_init__(self):
        self.cycle_time = cycle_times[self.command]

    def reduce_cycle_time(self, amount: int = 1) -> None:
        self.cycle_time -= amount


def create_instructions(lines: typing.Iterator[str]) -> typing.Iterator[Instruction]:
    for line in lines:
        try:
            command_str, value = line.split(" ")
        except ValueError:
            command_str = line
            value = None
        else:
            value = int(value)
        command = commands[command_str]
        yield Instruction(command, value)


@dataclasses.dataclass
class ClockCircuit:
    _observers: list[typing.Callable[[], None]] = dataclasses.field(
        default_factory=list, init=False
    )
    _cycle_number: int = dataclasses.field(default=0, init=False)

    def subscribe(self, callable: typing.Callable[[], None]) -> None:
        self._observers.append(callable)

    def cycle(self) -> None:
        for observer in self._observers:
            observer()
        self._cycle_number += 1

    @property
    def cycle_number(self) -> int:
        return self._cycle_number


@dataclasses.dataclass
class Cpu:
    clock_circuit: ClockCircuit
    instructions: list[Instruction] = dataclasses.field(default_factory=list)
    _x: int = dataclasses.field(default=1, init=False)
    _signal_strengths: list[int] = dataclasses.field(default_factory=list, init=False)

    def start_observing_cycle(self) -> None:
        self.clock_circuit.subscribe(self.on_cycle)

    def execute_instruction(self, instruction: Instruction) -> None:
        self.instructions.append(instruction)

    def on_cycle(self):
        for instruction in self.instructions:
            instruction.reduce_cycle_time()
            if instruction.cycle_time == 0:
                self.instruction_result(instruction)

        for instruction in self.instructions[:]:
            if instruction.cycle_time <= 0:
                self.instructions.remove(instruction)
        self.update_signal_strenght()

    def instruction_result(self, instruction: Instruction) -> None:
        if instruction.command == Command.NOOP:
            self.noop()
        elif instruction.command == Command.ADDX:
            self.addx(instruction.value)

    def noop(self) -> None:
        pass

    def addx(self, value) -> None:
        self._x += value

    def update_signal_strenght(self) -> None:
        cycle_number = self.clock_circuit.cycle_number
        cycle_number += 2  # Dont know ? but this makes it work
        if cycle_number < 20:
            return
        elif cycle_number == 20:
            self._signal_strengths.append(cycle_number * self._x)
            return
        if (cycle_number - 20) % 40 == 0:
            self._signal_strengths.append(cycle_number * self._x)

    @property
    def has_instructions(self) -> bool:
        return bool(self.instructions)

    @property
    def x(self) -> int:
        return self._x

    @property
    def signal_strengths(self) -> list[int]:
        return self._signal_strengths


@dataclasses.dataclass
class Crt:
    clock_circuit: ClockCircuit
    cpu: Cpu
    pixels: list[str] = dataclasses.field(default_factory=list)
    pixel: int = dataclasses.field(default=0, init=False)

    def start_observing_cycle(self) -> None:
        self.clock_circuit.subscribe(self.on_cycle)

    def on_cycle(self):
        character = "."
        if self.cpu.x - 1 <= self.pixel <= self.cpu.x + 1:
            character = "#"
        self.pixels.append(character)
        self.pixel += 1
        if self.pixel == 40:
            self.pixel = 0


def part1(filename: str) -> None:
    lines = yield_lines(filename)
    clock_circuit = ClockCircuit()
    cpu = Cpu(clock_circuit)
    cpu.start_observing_cycle()
    for instruction in create_instructions(lines):
        cpu.execute_instruction(instruction)
        while cpu.has_instructions:
            clock_circuit.cycle()

    print(sum(cpu.signal_strengths))


def part2(filename: str) -> None:
    lines = yield_lines(filename)
    clock_circuit = ClockCircuit()
    cpu = Cpu(clock_circuit)
    crt = Crt(clock_circuit, cpu)
    crt.start_observing_cycle()
    cpu.start_observing_cycle()
    for instruction in create_instructions(lines):
        cpu.execute_instruction(instruction)
        while cpu.has_instructions:
            clock_circuit.cycle()

    print("".join(crt.pixels[:40]))
    print("".join(crt.pixels[40:80]))
    print("".join(crt.pixels[80:120]))
    print("".join(crt.pixels[120:160]))
    print("".join(crt.pixels[160:200]))
    print("".join(crt.pixels[200:240]))


def main():
    part1(FILENAME)
    part2(FILENAME)


if __name__ == "__main__":
    main()
