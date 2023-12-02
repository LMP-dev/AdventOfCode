from pathlib import Path
import re

DATA_FILE_NAME = "input.txt"
INPUT_FILE = Path(__file__).parent / DATA_FILE_NAME
TEST_FILE_NAME = "example_3.txt"
TEST_INPUT_FILE = Path(__file__).parent / TEST_FILE_NAME


def parse_input(file_path: Path) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def is_it_a_number(character: str) -> tuple[bool, int | str]:
    try:
        number = int(character)
    except ValueError:
        return (False, character)
    else:
        return (True, number)


WRITTEN_DIGIT = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
REVERSED_WRITTEN_DIGIT = [word[::-1] for word in WRITTEN_DIGIT]
DIGITS_MAPPING = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

"""
example 3
92
11
11
28
"""


def solve_02(data: list[str]) -> int:
    calibration_values = []
    for line in data:
        first = None  # left to right
        last = None  # right to left
        partial_digits = ["", "", "", "", "", "", "", "", ""]
        partial_word = ""
        # Left to right loop
        for char in line:
            # Check digit
            is_number, val = is_it_a_number(char)
            if is_number:
                # Digit found, stop loop
                first = val
                break
            # Check written digits
            partial_word += char
            if partial_word in WRITTEN_DIGIT:
                # Found digit in written form, store and stop loop
                first = DIGITS_MAPPING[partial_word]
                break
            else:
                found_partial_match = False
                for word in WRITTEN_DIGIT:
                    if word.startswith(partial_word):
                        found_partial_match = True
                        break  # stops loop from one to nine check
                if not found_partial_match:
                    # Reset partial word
                    partial_word = char

        # Right to left loop
        partial_word = ""  # reset variable
        partial_digits = ["", "", "", "", "", "", "", "", ""]  # Reset variable
        for char in reversed(line):
            # Check digit
            is_number, val = is_it_a_number(char)
            if is_number:
                # Digit found, stop loop
                last = val
                break
            # Check written digits
            # partial_word += char
            partial_digits = [partial + char for partial in partial_digits]
            for partial in partial_digits:
                if partial in REVERSED_WRITTEN_DIGIT:
                    last = DIGITS_MAPPING[partial[::-1]]
                    break
            if last:
                break
            # Check if partially there is some match with a digit
            found_partial_match = False
            for i, (word, partial) in enumerate(
                zip(REVERSED_WRITTEN_DIGIT, partial_digits)
            ):
                if word.startswith(partial):
                    found_partial_match = True
                else:
                    # Reset partial word
                    partial_digits[i] = char
        print(calibration_values)
        calibration_values.append(10 * first + last)
    return sum(calibration_values)


def main() -> None:
    data = parse_input(TEST_INPUT_FILE)
    solution = solve_02(data)
    print(solution)  # 54140 (too high)
    # lines 3 (one less) and 7 wrong (one more)


if __name__ == "__main__":
    main()
