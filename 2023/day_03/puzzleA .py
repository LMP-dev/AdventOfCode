from pathlib import Path
from typing import Iterator

DATA_FILE_NAME = "input.txt"
DATA_TEST_FILE_NAME = "example_1.txt"
INPUT_FILE = Path(__file__).parent / DATA_FILE_NAME
TEST_INPUT_FILE = Path(__file__).parent / DATA_TEST_FILE_NAME


def parse_input(file_path: Path) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def solve_01(data: list[str]) -> int:
    # variables initialization
    part_numbers: set[int] = set()  # Assuming no repeated Part nº.
    last_row_numbers_data: list[tuple[int, list[int]]] = []
    last_row_symbol_indexes: list[int] = []
    for row in data:
        # variables initialization
        partial_number: str = ""
        number_columns: list[int] = []
        is_after_symbol: bool = False
        current_row_numbers_data: list[tuple[int, list[int]]] = []
        current_row_symbol_indexes: list[int] = []
        for index, char in enumerate(row):
            # char is a digit:
            if char.isnumeric():
                # Check if last char was a symbol
                if index - 1 in current_row_symbol_indexes:
                    is_after_symbol = True
                partial_number += char
                number_columns.append(index)
            # char is a symbol:
            elif char != ".":
                current_row_symbol_indexes.append(index)
                # Check number in current row
                if partial_number:
                    number = int(partial_number)
                    part_numbers.add(number)
                    current_row_numbers_data.append((number, number_columns))
                    # Reset variables
                    partial_number = ""  # reset
                    number_columns = []  # reset
                    is_after_symbol = False
                # Check number in last row
                for num_data in last_row_numbers_data:
                    if is_num_in_range(index, num_data[1]):
                        part_numbers.add(num_data[0])
            # char is a ".":
            else:
                # Check if is after a number
                if partial_number:
                    number = int(partial_number)
                    last_row_numbers_data.append((number, number_columns))
                    # Check if there was a symbol before the number
                    if is_after_symbol:
                        part_numbers.add(number)
                    else:
                        # Check symbols in last row
                        for i in last_row_symbol_indexes:
                            if is_num_in_range(i, number_columns):
                                part_numbers.add(number)
                    # Reset variables
                    partial_number = ""  # reset
                    number_columns = []  # reset
                    is_after_symbol = False
        # edge case where number is end of row:
        ...

        # Update last row references
        last_row_numbers_data = current_row_numbers_data
        last_row_symbol_indexes = current_row_symbol_indexes
    print(part_numbers)
    return sum(part_numbers)


def is_num_in_range(char_index: int, number_indixes: Iterator[int]) -> bool:
    """Function to check numbers on rows top or below a character row"""
    position_to_check = [char_index - 1, char_index, char_index + 1]
    for pos in position_to_check:
        if pos in number_indixes:
            return True
    return False


def main() -> None:
    data = parse_input(TEST_INPUT_FILE)
    solution = solve_01(data)
    print(solution)
    """Numbers test not detected:
    467, 633, 755, 598"""


if __name__ == "__main__":
    main()
