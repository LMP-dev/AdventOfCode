# Standard library
from pathlib import Path
from typing import Any

INPUT_FILE_PATH = Path(__file__).parent


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def parse_input(file_content: list[str]) -> list[list[str]]:
    diagram = []

    for line in file_content:
        diagram.append([char for char in line])

    return diagram


class TachyonMainfold:
    def __init__(
        self, diagram: list[list[str]], starting_point: tuple[int, int]
    ) -> None:
        self.diagram = diagram
        self.starting_point = starting_point
        self.max_row = len(diagram) - 1

    def enter_beam(self) -> int:
        """Returns the number of times a beam splits"""
        # Initiate variables
        self.split_counter = 0
        locations_to_advance: list[tuple[int, int]] = [self.starting_point]
        visited_locations: set[tuple[int, int]] = set()

        while locations_to_advance:
            # Extract a location to visit and process it
            location = locations_to_advance.pop()
            next_location = (location[0] + 1, location[1])

            if next_location[0] == self.max_row:
                continue  # arrived to last row
            if self.diagram[next_location[0]][next_location[1]] == ".":
                if next_location in visited_locations:
                    continue  # reached a path already walked
                else:
                    visited_locations.add(next_location)
                    locations_to_advance.append(next_location)
            elif self.diagram[next_location[0]][next_location[1]] == "^":
                self.split_counter += 1
                left_location = (next_location[0], next_location[1] - 1)
                rigth_location = (next_location[0], next_location[1] + 1)
                if left_location not in visited_locations:
                    visited_locations.add(left_location)
                    locations_to_advance.append(left_location)
                if rigth_location not in visited_locations:
                    visited_locations.add(rigth_location)
                    locations_to_advance.append(rigth_location)
            else:
                raise Exception(
                    f"Found incorrect symbol: {self.diagram[next_location[0]][next_location[1]]} !"
                )

        return self.split_counter


def solve_02(data: list[list[str]]) -> int:
    """
    Assumptions:
        - No beam gets outside of diagram when splitting
        - Last row is all "."
    """
    # Find starting position
    for index, char in enumerate(data[0]):
        if char == "S":
            starting_point = (0, index)

    tachyon_mainfold = TachyonMainfold(data, starting_point)

    return tachyon_mainfold.enter_beam()


def main() -> None:
    # input.txt | example_1.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_02(data)
    print(f"The solution of the example 1 is {solution}")  # Solution 40
    file_content = read_data(INPUT_FILE_PATH / "input.txt")
    data = parse_input(file_content)
    solution = solve_02(data)
    print(f"The solution of the part 2 is {solution}")  # Solution ...


if __name__ == "__main__":
    main()
