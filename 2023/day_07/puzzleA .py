# Standard library
from pathlib import Path


# Own modules
from hand import Hand, HandType, create_hand_object

INPUT_FILE_PATH = Path(__file__).parent


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def convert_to_tuple_hand(hand: str) -> tuple[int, int, int, int, int]:
    mapping = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "J": 11,
        "T": 10,
        "9": 9,
        "8": 8,
        "7": 7,
        "6": 6,
        "5": 5,
        "4": 4,
        "3": 3,
        "2": 2,
    }

    converted_hand = []
    for card in hand:
        converted_hand.append(mapping[card])
    return tuple(converted_hand)


def find_hand_category(hand: tuple[int, int, int, int, int]) -> HandType:
    ...


def parse_input(file_content: list[str]) -> list[Hand]:
    hands = []
    for line in file_content:
        hand_str, bid = line.split(" ")
        hand_tuple = convert_to_tuple_hand(hand_str)
        hand_type = find_hand_category(hand_tuple)
        hand_object = create_hand_object(hand_tuple, hand_type)
        hands.append(hand_object)
    return hands


def solve_01(data: list[Hand]) -> int:
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
