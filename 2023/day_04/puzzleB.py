from pathlib import Path
from functools import lru_cache

import numpy as np

INPUT_FILE_PATH = Path(__file__).parent


def parse_input(file_path: Path) -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    # Utility function
    def convert_to_int_list(string_list: list[str]) -> list[int]:
        number_list = []
        for string in string_list:
            if string:
                number_list.append(int(string))
        return number_list

    # parse_input
    scratch_cards = []
    with open(file_path) as file:
        for raw_line in file:
            line = raw_line.strip()
            _, card_numbers_section = line.split(":")
            # numbers parsing
            winning_numbers_section, own_numbers_section = card_numbers_section.split(
                "|"
            )
            # List creation
            winning_numbers = convert_to_int_list(
                winning_numbers_section.strip().split(" ")
            )
            own_numbers = convert_to_int_list(own_numbers_section.strip().split(" "))
            scratch_cards.append((tuple(winning_numbers), tuple(own_numbers)))
    return scratch_cards


def solve_01(data: list[tuple[tuple[int, ...], tuple[int, ...]]]) -> int:
    # variables initialization
    scratch_cards_count = np.ones(len(data))  # stores nº of cards and copies

    for id, (winning, own) in enumerate(data):
        matches = find_matches(winning, own)
        # Create copies
        for i in range(matches):
            scratch_cards_count[id + i + 1] = (
                scratch_cards_count[id + i + 1] + 1 * scratch_cards_count[id]
            )
    return np.sum(scratch_cards_count)


@lru_cache
def find_matches(first_list: tuple[int], second_list: tuple[int]) -> int:
    matches = 0
    for number in second_list:
        if number in first_list:
            matches += 1
    return matches


def main() -> None:
    # input.txt | example_1.txt | example_2.txt
    data = parse_input(INPUT_FILE_PATH / "example_1.txt")
    solution = solve_01(data)
    print(f"The solution of the example is {solution}")
    data = parse_input(INPUT_FILE_PATH / "input.txt")
    solution = solve_01(data)  # 14427616
    print(f"The solution of part 1 is {solution}")


if __name__ == "__main__":
    main()
