# Standard library
from pathlib import Path


# Own modules
from hand import (
    Hand,
    HandType,
    convert_to_numerical_hand,
    create_hand_object,
    find_hand_category,
)

INPUT_FILE_PATH = Path(__file__).parent


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def parse_input(file_content: list[str]) -> list[tuple[Hand, int]]:
    hands = []
    for line in file_content:
        hand_str, bid = line.split(" ")
        hand_tuple = convert_to_numerical_hand(hand_str)
        hand_type = find_hand_category(hand_tuple)
        hand_object = create_hand_object(hand_tuple, hand_type)
        hands.append((hand_object, bid))
    return hands


def solve_01(data: list[tuple[Hand, int]]) -> int:
    return


def main() -> None:
    # input.txt | example_1.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of the example is {solution}")
    file_content = read_data(INPUT_FILE_PATH / "input.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of part 1 is {solution}")


if __name__ == "__main__":
    main()
