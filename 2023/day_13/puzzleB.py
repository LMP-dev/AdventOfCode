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
    # for loop poping first and last elements and checking they are equal!
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


def fix_smudge_pattern(pattern: list[list[str]]) -> list[list[str]] | None:
    def only_one_difference(row_1: list[str], row_2: list[str]) -> int | None:
        difference = []
        for i, (x, y) in enumerate(zip(row_1, row_2)):
            if x != y:
                difference.append(i)
        if len(difference) == 1:
            return difference[0]
    
    def fix_smudge(row: list[str], index: int) -> None:
        '''Modifies the same list it recives'''
        fixer = {".": "#", "#":"."}
        row[index] = fixer[row[index]]

    # Find position of the smudge to fix
    temp_pattern = pattern.copy()
    row_index = 0
    while temp_pattern:
        row = temp_pattern.pop(0)
        for other_row in temp_pattern:
            index_smudge = only_one_difference(row, other_row)
            if index_smudge is not None:
                break
        if index_smudge is not None:
            break
        row_index += 1
    
    # Fix the smudge
    if index_smudge is not None:
        new_pattern = pattern.copy()
        fix_smudge(new_pattern[row_index], index_smudge)
        return new_pattern
    return None


def solve_02(data: list[list[list[str]]]) -> int:
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

        # Fix smudge on the mirror
        new_pattern = fix_smudge_pattern(pattern)
        if new_pattern:
            # Look rows and then columns
            ...
        else:
            # fix_smudge for columns and look columns and rows
            ...
        
        print(f"Pattern with fixed smudge is:\n{new_pattern}")

    return pattern_notes


def main() -> None:
    # input.txt | example_1.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_02(data)
    print(f"The solution of the example 1 is {solution}")
    # file_content = read_data(INPUT_FILE_PATH / "input.txt")
    # data = parse_input(file_content)
    # solution = solve_02(data)
    # print(f"The solution of the part 1 is {solution}")


if __name__ == "__main__":
    main()
