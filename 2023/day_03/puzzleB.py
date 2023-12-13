from pathlib import Path
from typing import Iterator

INPUT_FILE_PATH = Path(__file__).parent


def parse_input(file_path: Path) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def solve_02(data: list[str]) -> int:
    """
    lines are:
        - top
        - middle
        - low (ALWAYS file pointer)
    Two special cases to take into account:
        · The 2 first lines (middle & low with no top - inside for loop)
        - The two last lines (top & middle - out of the for loop)
    """
    # variables initialization
    gear_ratios: list[int] = []
    top_row_numbers_data: list[tuple[int, list[int]]] = []
    middle_row_numbers_data: list[tuple[int, list[int]]] = []
    middle_row_symbol_indexes: list[int] = []
    low_row_numbers_data: list[tuple[int, list[int]]] = []
    low_row_symbol_indexes: list[int] = []
    for row in data:
        # variables initialization
        partial_number: str = ""
        number_columns: list[int] = []
        # Parse row
        for index, char in enumerate(row):
            # char is a digit:
            if char.isnumeric():
                partial_number += char
                number_columns.append(index)
            # char is a potential gear:
            elif char == "*":
                low_row_symbol_indexes.append(index)
                # Check if there is number in last position
                if partial_number:
                    number = int(partial_number)
                    low_row_numbers_data.append((number, number_columns))
                    # Reset variables
                    partial_number = ""  # reset
                    number_columns = []  # reset
            # char is all the others:
            else:
                # Check if is after a number
                if partial_number:
                    number = int(partial_number)
                    low_row_numbers_data.append((number, number_columns))
                    # Reset variables
                    partial_number = ""  # reset
                    number_columns = []  # reset
        # edge case where number is end of row:
        if partial_number:
            number = int(partial_number)
            low_row_numbers_data.append((number, number_columns))

        # Look for gears
        if not top_row_numbers_data and middle_row_symbol_indexes:  # Special case 1
            for symbol_index in middle_row_symbol_indexes:
                part_numbers: list[int] = []
                # Check middle row matches
                for number_data in middle_row_numbers_data:
                    if is_num_in_horizontal_range(symbol_index, number_data[1]):
                        part_numbers.append(number_data[0])
                # Checl low row matches
                for number_data in low_row_numbers_data:
                    if is_num_in_diagonal_range(symbol_index, number_data[1]):
                        part_numbers.append(number_data[0])

                # Check if it is a gear (only 2 part numbers)
                if len(part_numbers) == 2:
                    gear_ratios.append(part_numbers[0] * part_numbers[1])
        else:
            # General case (top, middle and low rows)
            for symbol_index in middle_row_symbol_indexes:
                part_numbers: list[int] = []
                # Check top row matches
                for number_data in top_row_numbers_data:
                    if is_num_in_diagonal_range(symbol_index, number_data[1]):
                        part_numbers.append(number_data[0])
                # Check middle row matches
                for number_data in middle_row_numbers_data:
                    if is_num_in_horizontal_range(symbol_index, number_data[1]):
                        part_numbers.append(number_data[0])
                # Check low row matches
                for number_data in low_row_numbers_data:
                    if is_num_in_diagonal_range(symbol_index, number_data[1]):
                        part_numbers.append(number_data[0])

                # Check if it is a gear (only 2 part numbers)
                if len(part_numbers) == 2:
                    gear_ratios.append(part_numbers[0] * part_numbers[1])

        # Update row references
        top_row_numbers_data = middle_row_numbers_data
        middle_row_numbers_data = low_row_numbers_data
        middle_row_symbol_indexes = low_row_symbol_indexes
        # Reset low row
        low_row_numbers_data = []
        low_row_symbol_indexes = []

    # Special case 2
    for symbol_index in middle_row_symbol_indexes:
        part_numbers: list[int] = []
        # Check top row matches
        for number_data in top_row_numbers_data:
            if is_num_in_diagonal_range(symbol_index, number_data[1]):
                part_numbers.append(number_data[0])
        # Checl middle row matches
        for number_data in middle_row_numbers_data:
            if is_num_in_horizontal_range(symbol_index, number_data[1]):
                part_numbers.append(number_data[0])

        # Check if it is a gear (only 2 part numbers)
        if len(part_numbers) == 2:
            gear_ratios.append(part_numbers[0] * part_numbers[1])

    return sum(gear_ratios)


def is_num_in_diagonal_range(char_index: int, number_indexes: Iterator[int]) -> bool:
    """Function to check numbers on rows top or below a symbol row"""
    positions_to_check = [char_index - 1, char_index, char_index + 1]
    for pos in positions_to_check:
        if pos in number_indexes:
            return True
    return False


def is_num_in_horizontal_range(char_index: int, number_indexes: Iterator[int]) -> bool:
    """Function to check numbers on same row of a symbol row"""
    positions_to_check = [char_index - 1, char_index + 1]
    for pos in positions_to_check:
        if pos in number_indexes:
            return True
    return False


def main() -> None:
    # input.txt | example_1.txt | example_2.txt
    data = parse_input(INPUT_FILE_PATH / "example_1.txt")
    solution = solve_02(data)
    print(f"The solution of the example is {solution}")
    data = parse_input(INPUT_FILE_PATH / "input.txt")
    solution = solve_02(data)
    print(f"The solution of part 2 is {solution}")


if __name__ == "__main__":
    main()
