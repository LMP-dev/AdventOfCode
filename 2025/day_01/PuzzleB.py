# Standard library
from pathlib import Path
from typing import Any
from dataclasses import dataclass

INPUT_FILE_PATH = Path(__file__).parent


@dataclass
class Dial099:
    current: int = 50

    zero_count: int = 0

    def find_0s(self, instructions: list[tuple[str, int]]) -> int:
        print(f"The dial points to {self.current}")
        for direction, number in instructions:
            ## Remove complete spins
            spins, rem = divmod(number, 100)  # 0 to 99 is 100 numbers

            if direction == "R":
                self._move_right(rem)
            elif direction == "L":
                self._move_left(rem)
            else:
                raise Exception(f"Incorrect direction (R,L): {direction}")

            if self.current == 0:
                self.zero_count += 1

        return self.zero_count

    def _move_left(self, positions: int):
        next_number = self.current - positions
        if next_number < 0:
            spins, rem = divmod(next_number, 99)
            self.current = rem + 1  # -1 --> 99 (rem=98)
        else:
            self.current = next_number

    def _move_right(self, positions: int):
        next_number = self.current + positions
        if next_number > 99:
            spins, rem = divmod(next_number, 99)
            self.current = rem - 1  # 100 --> 0 (rem = 1)
        else:
            self.current = next_number


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def parse_input(file_content: list[str]) -> list[tuple[str, int]]:
    instructions = [(line[0], int(line[1:])) for line in file_content]
    return instructions


def solve(data: Any) -> int:
    dial = Dial099()

    count = dial.find_0s(data)

    return count


def main() -> None:
    # input.txt | example_1.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve(data)
    print(f"The solution of the example 1 is {solution}")
    file_content = read_data(INPUT_FILE_PATH / "input.txt")
    data = parse_input(file_content)
    solution = solve(data)
    print(f"The solution of the part 1 is {solution}")


if __name__ == "__main__":
    main()
