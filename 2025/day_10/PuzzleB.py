# Standard library
from pathlib import Path
from typing import Any
import numpy as np
from itertools import combinations


INPUT_FILE_PATH = Path(__file__).parent


class MachineJoltage:
    def __init__(
        self,
        buttons_schematic: list[tuple[int, ...]],
        joltage_requirements: tuple[int, ...],
    ):
        self.schematics = buttons_schematic
        self.requirements = joltage_requirements


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def parse_input(file_content: list[str]) -> list[MachineJoltage]:
    """Avoiding light diagram"""
    machines: list[dict[str, np.ndarray | list[np.ndarray]]] = []
    for line in file_content:
        _, *raw_schematics, raw_requirements = line.split()

        # Transform joltage requirements
        joltage_requirements = eval("(" + raw_requirements[1:-1] + ")")

        # Transform schematics to binary vectors
        buttons_schematic = []
        for str_schematic in raw_schematics:
            scheme = eval(str_schematic)
            if type(scheme) is int:
                scheme = tuple([scheme])  # special case for only 1 element in tuple
            buttons_schematic.append(scheme)

        # Store machine data
        machines.append(MachineJoltage(buttons_schematic, joltage_requirements))

    return machines


def solve_02(data: Any) -> int:
    return


def main() -> None:
    # input.txt | example_1.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_02(data)
    print(f"The solution of the example 1 is {solution}")
    file_content = read_data(INPUT_FILE_PATH / "input.txt")
    data = parse_input(file_content)
    solution = solve_02(data)
    print(f"The solution of the part 2 is {solution}")


if __name__ == "__main__":
    main()
