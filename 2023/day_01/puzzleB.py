from pathlib import Path
import re

DATA_FILE_NAME = "input.txt"
INPUT_FILE = Path(__file__).parent / DATA_FILE_NAME
TEST_INPUT_FILE = Path(__file__).parent / "example_2.txt"


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


def solve_02(data: list[str]) -> int:
    calibration_values = []
    for line in data:
        first = None  # left to right
        last = None  # right to left
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
        for char in reversed(line):
            # Check digit
            is_number, val = is_it_a_number(char)
            if is_number:
                # Digit found, stop loop
                last = val
                break
            # Check written digits
            partial_word += char
            if partial_word in REVERSED_WRITTEN_DIGIT:
                # Found digit in written form, store and stop loop
                last = DIGITS_MAPPING[partial_word[::-1]]
                break
            else:
                found_partial_match = False
                for word in REVERSED_WRITTEN_DIGIT:
                    if word.startswith(partial_word):
                        found_partial_match = True
                        break  # stops loop from one to nine check
                if not found_partial_match:
                    # Reset partial word
                    partial_word = char

        calibration_values.append(10 * first + last)
    return sum(calibration_values)


def main() -> None:
    data = parse_input(INPUT_FILE)
    solution = solve_02(data)
    print(solution)  # 54140 (too high)
    # lines 3 (one less) and 7 wrong (one more)


if __name__ == "__main__":
    main()
