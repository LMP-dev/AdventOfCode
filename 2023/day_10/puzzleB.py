# Standard library
from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass
from enum import Enum, auto

INPUT_FILE_PATH = Path(__file__).parent


class Direction(Enum):
    NORD = auto()
    EAST = auto()
    SUD = auto()
    WEST = auto()


@dataclass
class AnimalPosition:
    """position = (row, column) - (0,0) starts at the left-top corner of the grid"""

    row: int
    col: int
    to_direction: Direction

    def next_position(self, pipes_map: list[list[str]]) -> AnimalPosition | None:
        max_row = len(pipes_map) - 1
        max_column = len(pipes_map[0]) - 1
        # Check out of bound movement
        if self.to_direction == Direction.NORD:
            new_row = self.row - 1
            if new_row < 0:
                return None
            new_col = self.col
        elif self.to_direction == Direction.EAST:
            new_col = self.col + 1
            if new_col > max_column:
                return None
            new_row = self.row
        elif self.to_direction == Direction.SUD:
            new_row = self.row + 1
            if new_row > max_row:
                return None
            new_col = self.col
        elif self.to_direction == Direction.WEST:
            new_col = self.col - 1
            if new_col < 0:
                return None
            new_row = self.row
        # Get new tile and check movement
        tile = pipes_map[new_row][new_col]
        if tile == ".":
            # Ground no entrances
            return None
        elif tile == "|":
            # Vertical directions will continue the same path
            if (
                self.to_direction == Direction.EAST
                or self.to_direction == Direction.WEST
            ):
                return None
            else:
                return AnimalPosition(new_row, new_col, self.to_direction)
        elif tile == "-":
            # Horizontal directions will continue the same path
            if (
                self.to_direction == Direction.NORD
                or self.to_direction == Direction.SUD
            ):
                return None
            else:
                return AnimalPosition(new_row, new_col, self.to_direction)
        elif tile == "L":
            # Entrances in sud direction and west direction
            if (
                self.to_direction == Direction.EAST
                or self.to_direction == Direction.NORD
            ):
                return None
            else:
                if self.to_direction == Direction.SUD:
                    return AnimalPosition(new_row, new_col, Direction.EAST)
                elif self.to_direction == Direction.WEST:
                    return AnimalPosition(new_row, new_col, Direction.NORD)
        elif tile == "J":
            # Entrances in sud direction and east direction
            if (
                self.to_direction == Direction.WEST
                or self.to_direction == Direction.NORD
            ):
                return None
            else:
                if self.to_direction == Direction.SUD:
                    return AnimalPosition(new_row, new_col, Direction.WEST)
                elif self.to_direction == Direction.EAST:
                    return AnimalPosition(new_row, new_col, Direction.NORD)
        elif tile == "7":
            # Entrances in nord direction and east direction
            if (
                self.to_direction == Direction.WEST
                or self.to_direction == Direction.SUD
            ):
                return None
            else:
                if self.to_direction == Direction.NORD:
                    return AnimalPosition(new_row, new_col, Direction.WEST)
                elif self.to_direction == Direction.EAST:
                    return AnimalPosition(new_row, new_col, Direction.SUD)
        elif tile == "F":
            # Entrances in nord direction and west direction
            if (
                self.to_direction == Direction.EAST
                or self.to_direction == Direction.SUD
            ):
                return None
            else:
                if self.to_direction == Direction.NORD:
                    return AnimalPosition(new_row, new_col, Direction.EAST)
                elif self.to_direction == Direction.WEST:
                    return AnimalPosition(new_row, new_col, Direction.SUD)
        else:
            raise Exception(f"Unknown tile found: {tile}")


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def parse_input(file_content: list[str]) -> tuple[list[list[str]], tuple[int, int]]:
    grid = []
    for r, grid_line in enumerate(file_content):
        new_row = []
        for c, char in enumerate(grid_line):
            new_row.append(char)
            if char == "S":
                start_position = (r, c)
        grid.append(new_row)
    return grid, start_position


def solve_02(data: tuple[list[list[str]], tuple[int, int]]) -> int:
    # Unpack data
    pipes_map, start_position = data
    row, col = start_position
    # Initialize variables
    visited_positions: list[tuple[int, int]] = [start_position]
    animal_positions = [
        AnimalPosition(row, col, to_direction=Direction.NORD),
        AnimalPosition(row, col, to_direction=Direction.EAST),
        AnimalPosition(row, col, to_direction=Direction.SUD),
        AnimalPosition(row, col, to_direction=Direction.WEST),
    ]
    looking = True
    # Initialize variables for reconstructing graph
    from_neighbour: list[tuple[int, int]] = [
        None
    ]  # paralel list to visited_positions with coming position of that node
    final_neighbour: tuple[int, int] = None
    final_position: tuple[int, int] = None

    while looking:
        new_animal_positions: list[AnimalPosition] = []
        for animal_position in animal_positions:
            new_animal_position = animal_position.next_position(
                pipes_map
            )  # may return None if invalid movement
            from_position = (animal_position.row, animal_position.col)
            if not new_animal_position:
                continue
            new_position = (new_animal_position.row, new_animal_position.col)
            if new_position in visited_positions:
                # found farthest position
                looking = False
                final_position = new_position
                final_neighbour = from_position
                break
            else:
                visited_positions.append(new_position)
                from_neighbour.append(from_position)
                new_animal_positions.append(new_animal_position)
        animal_positions = new_animal_positions

    # Create graph of the path
    i = visited_positions.index(final_position)
    final_other_neighbour = from_neighbour[i]

    graph = {
        final_position: [final_neighbour, final_other_neighbour],
        final_neighbour: [final_position],
        final_other_neighbour: [final_position],
    }
    to_be_visited = [final_neighbour, final_other_neighbour]
    while to_be_visited:
        node = to_be_visited.pop()
        i = visited_positions.index(node)
        neighbour_node = from_neighbour[i]

        if node in graph.keys():
            if neighbour_node:
                graph[node].append(neighbour_node)
        else:
            graph.update({node: [neighbour_node]})
        if neighbour_node:
            if neighbour_node in graph.keys():
                graph[neighbour_node].append(node)
            else:
                graph.update({neighbour_node: [node]})

            to_be_visited.append(neighbour_node)

    # Find enclosed cells in the loop

    return graph


def main() -> None:
    # input.txt | example_1.txt | example_1_v2.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_02(data)
    print(f"The solution of the example 1 is {solution}")
    file_content = read_data(INPUT_FILE_PATH / "example_2.txt")
    data = parse_input(file_content)
    solution = solve_02(data)
    print(f"The solution of the example 2 is {solution}")
    # file_content = read_data(INPUT_FILE_PATH / "example_3.txt")
    # data = parse_input(file_content)
    # solution = solve_02(data)
    # print(f"The solution of the example 3 is {solution}")
    # file_content = read_data(INPUT_FILE_PATH / "example_4.txt")
    # data = parse_input(file_content)
    # solution = solve_02(data)
    # print(f"The solution of the example 4 is {solution}")
    # file_content = read_data(INPUT_FILE_PATH / "example_5.txt")
    # data = parse_input(file_content)
    # solution = solve_02(data)
    # print(f"The solution of the example 5 is {solution}")
    # file_content = read_data(INPUT_FILE_PATH / "input.txt")
    # data = parse_input(file_content)
    # solution = solve_02(data)
    # print(f"The solution of the part 2 is {solution}")


if __name__ == "__main__":
    main()
