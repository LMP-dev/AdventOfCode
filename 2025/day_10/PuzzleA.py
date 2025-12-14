# Standard library
from pathlib import Path
from typing import Any
import numpy as np

INPUT_FILE_PATH = Path(__file__).parent


class Machine:
    def __init__(
        self,
        light_diagram: np.ndarray,
        buttons_schematic: list[np.ndarray],
        joltage_requirements: Any,
    ):
        self.diagram = light_diagram
        self.schematics = buttons_schematic
        self.requirements = joltage_requirements


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def parse_input(file_content: list[str]) -> list[Machine]:
    """Avoiding joltage requirements"""
    machines: list[dict[str, np.ndarray | list[np.ndarray]]] = []
    for line in file_content:
        raw_diagram, *raw_schematics, raw_requirements = line.split()

        # Transform diagram to binary vector
        light_diagram = np.array(
            np.zeros(len(raw_diagram) - 2), dtype=bool
        )  # -2 to consider brackets []
        for i, char in enumerate(raw_diagram[1:-1]):
            if char == "#":
                light_diagram[i] = True

        # Transform schematics to binary vectors
        buttons_schematic = []
        for str_schematic in raw_schematics:
            scheme = eval(str_schematic)
            if type(scheme) is int:
                scheme = tuple([scheme])  # special case for only 1 element in tuple
            button_scheme = np.zeros(len(light_diagram), dtype=bool)
            for index in scheme:
                button_scheme[index] = True
            buttons_schematic.append(button_scheme)

        # Store machine data
        machines.append(Machine(light_diagram, buttons_schematic, raw_requirements))

    return machines


def solve_01(data: list[Machine]) -> int:
    print(f"The first machine have diagram: {data[0].diagram}")
    print(f"The first machine have buttons schematics: {data[0].schematics}")
    return


def main() -> None:
    # input.txt | example_1.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of the example 1 is {solution}")  # Solution 7
    # file_content = read_data(INPUT_FILE_PATH / "input.txt")
    # data = parse_input(file_content)
    # solution = solve_01(data)
    # print(f"The solution of the part 1 is {solution}")  # Solution


if __name__ == "__main__":
    main()
