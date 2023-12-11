# Standard library
from pathlib import Path

# Own modules
from hand import Hand, convert_to_numerical_hand, create_hand_object, find_hand_category

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
        hands.append((hand_object, int(bid)))
    return hands


def solve_01(data: list[tuple[Hand, int]]) -> int:
    total_winnings = 0

    ranks = [(hand.points(), bid) for hand, bid in data]
    ranks.sort()

    for i, item in enumerate(ranks):
        _, bid = item
        total_winnings += (i + 1) * bid
    return total_winnings


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
    """
    1 - 2   10
    2 - 3   21
    3 - 5   65
    4 - 4   68
    5 - 11  297
    6 - 10  230
    7 - 1   3
    8 - 7   231
    9 - 6   246
    10 - 8  448
    11 - 9  702
    total = 2321
    """
    file_content = read_data(INPUT_FILE_PATH / "example_3.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of the example 3 is {solution}")


if __name__ == "__main__":
    main()
