from pathlib import Path

INPUT_FILE = Path(__file__).parent / "input.txt"
# INPUT_FILE = Path(__file__).parent / "test_input.txt"
# INPUT_FILE = Path(__file__).parent / "large_test_input.txt"


class Clockcircuit:
    def __init__(self) -> None:
        self.cycle = 1
        self.register = 1
        self.signal_strenght = list()

    def noop(self) -> None:
        self._check_signal_strenght()
        self.cycle += 1

    def addx(self, v: int) -> None:
        self._check_signal_strenght()
        self.cycle += 1
        self._check_signal_strenght()
        self.cycle += 1
        self.register += v

    def _check_signal_strenght(self) -> None:
        if (self.cycle - 20) % 40 == 0:
            sign_strength = self.register * self.cycle
            print(
                f"During cycle {self.cycle}, the x register has the value {self.register} and signal strength is {sign_strength}"
            )
            self.signal_strenght.append(sign_strength)

    def sum_signal_strenght(self) -> int:
        return sum(self.signal_strenght)


def main() -> None:
    clock = Clockcircuit()
    with open(INPUT_FILE, "r") as file:
        for line in file:
            command, *v = line.split()
            if command == "noop":
                clock.noop()
            elif command == "addx":
                clock.addx(int(v[0]))
    clock._check_signal_strenght()
    print(clock.sum_signal_strenght())


if __name__ == "__main__":
    main()
