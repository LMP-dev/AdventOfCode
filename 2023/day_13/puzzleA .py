# Standard library
from pathlib import Path
import math

INPUT_FILE_PATH = Path(__file__).parent


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def parse_input(file_content: list[str]) -> list[list[list[str]]]:
    patterns = []
    pattern = []
    for line in file_content:
        if line:
            pattern.append(list(line))
        else:
            patterns.append(pattern)
            pattern = list()
    patterns.append(pattern)
    return patterns


def check_symmetry_between_rows(
    start_row: int, end_row: int, pattern: list[list[str]]
) -> int | None:
    mirror_area = pattern[start_row : end_row + 1]
    if len(mirror_area) % 2 != 0:
        return None
    while mirror_area:
        last_row = mirror_area.pop()
        first_row = mirror_area.pop(0)
        if first_row != last_row:
            return None
    difference = end_row - start_row
    lower_row = start_row + math.floor(difference / 2)

    return lower_row + 1  # Problem rows start at 1 not at 0


def find_row_symmetry(pattern: list[list[str]]) -> int | None:
    sym_row = None
    max_index = len(pattern) - 1
    # Check horizontal symmetry
    for line in pattern:
        if sym_row:
            break
        count = pattern.count(line)
        if count == 1:
            continue
        else:
            indices = [i for i, val in enumerate(pattern) if val == line]
            # Not in one of the edges of the pattern
            if not (0 in indices or max_index in indices):
                continue
            # First match is in edge of pattern
            if indices[0] == 0:
                for index in indices[1:]:
                    row = check_symmetry_between_rows(0, index, pattern)
                    if row:
                        sym_row = row
                        break
            # Last match is in edge of pattern
            if indices[-1] == max_index:
                for index in indices[:-1]:
                    row = check_symmetry_between_rows(index, max_index, pattern)
                    if row:
                        sym_row = row
                        break

    return sym_row


def solve_01(data: list[list[list[str]]]) -> int:
    pattern_notes = 0
    for pattern in data:
        # Search for horizontal symmetry
        row_symmetry = find_row_symmetry(pattern)
        if row_symmetry:
            pattern_notes += 100 * row_symmetry
        else:
            # Search for vertical symmetry
            col_pattern = list(zip(*pattern))
            col_symmetry = find_row_symmetry(col_pattern)
            if not col_symmetry:
                raise Exception(
                    f"No horizontal and vertical symmetries found in the pattern:\n{pattern}"
                )
            pattern_notes += col_symmetry

    return pattern_notes


def main() -> None:
    # input.txt | example_1.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of the example 1 is {solution}")
    file_content = read_data(INPUT_FILE_PATH / "input.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of the part 1 is {solution}")


if __name__ == "__main__":
    main()
