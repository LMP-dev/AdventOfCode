# Standard library
from pathlib import Path

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


def check_symmetry_between_elements(
    start_line, end_line, pattern: list[list[str]]
) -> tuple[bool, int]:
    return


def find_row_symmetry(pattern: list[list[str]]) -> int | None:
    row = None
    # Check horizontal symmetry
    for line in pattern:
        count = pattern.count(line)
        if count == 1:
            continue
        else:
            indices = [i for i, val in enumerate(pattern) if val == line]
            if count == 2:
                is_sym, row_sym = check_symmetry_between_elements(
                    indices[0], indices[1], pattern
                )
                if is_sym:
                    row == row_sym
                    break
            else:
                # Should consider case for par and odd
                ...
    return row


def solve_01(data: list[list[list[str]]]) -> int:
    pattern_notes = 0
    for pattern in data:
        row_symmetry = find_row_symmetry(pattern)
        if row_symmetry:
            pattern_notes += 100 * row_symmetry
        else:
            col_pattern = list(zip(*pattern))
            col_symmetry = find_row_symmetry(col_pattern)
            if not col_symmetry:
                raise Exception(f"No symmetry found in the pattern:\n{pattern}")
            pattern_notes += col_symmetry

    return pattern_notes


def main() -> None:
    # input.txt | example_1.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of the example 1 is {solution}")
    # file_content = read_data(INPUT_FILE_PATH / "input.txt")
    # data = parse_input(file_content)
    # solution = solve_01(data)
    # print(f"The solution of the part 1 is {solution}")


if __name__ == "__main__":
    main()
