# Standard library
from pathlib import Path
from typing import Any
import numpy as np
from itertools import combinations

INPUT_FILE_PATH = Path(__file__).parent


class MachineDiagram:
    def __init__(
        self,
        light_diagram: np.ndarray,
        buttons_schematic: list[np.ndarray],
    ):
        self.diagram = light_diagram
        self.schematics = buttons_schematic

        self.min_btn_pressed = None

    def calculate_min_btn_pressed(self) -> None:
        """Not considering same button repeated!"""
        num_buttons = 1
        match_found = False

        while not match_found:
            # Guard to avoid infinite loop
            if num_buttons > len(self.schematics):
                raise Exception(
                    "No combination of buttons found that creates the diagram"
                )

            # Check combinations
            for btn_group in combinations(self.schematics, num_buttons):
                # Operate
                result = np.zeros(len(self.diagram), dtype=bool)
                for button in btn_group:
                    result ^= button
                # Check
                if np.all(self.diagram == result):
                    match_found = True
                    break

            # INcrease counter combination size
            if not match_found:
                num_buttons += 1

        self.min_btn_pressed = num_buttons


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def parse_input(file_content: list[str]) -> list[MachineDiagram]:
    """Avoiding joltage requirements"""
    machines: list[dict[str, np.ndarray | list[np.ndarray]]] = []
    for line in file_content:
        raw_diagram, *raw_schematics, _ = line.split()

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
        machines.append(MachineDiagram(light_diagram, buttons_schematic))

    return machines


def solve_01(data: list[MachineDiagram]) -> int:
    count = 0
    for machine in data:
        machine.calculate_min_btn_pressed()
        count += machine.min_btn_pressed
    return count


def main() -> None:
    # input.txt | example_1.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of the example 1 is {solution}")  # Solution 7
    file_content = read_data(INPUT_FILE_PATH / "input.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of the part 1 is {solution}")  # Solution 434


if __name__ == "__main__":
    main()
