from pathlib import Path

INPUT_FILE_PATH = Path(__file__).parent


def parse_input(file_path: Path) -> list[tuple[list[int], list[int]]]:
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
            # Parsing numbers
            winning_numbers_section, own_numbers_section = card_numbers_section.split(
                "|"
            )
            # List creation
            winning_numbers = convert_to_int_list(
                winning_numbers_section.strip().split(" ")
            )
            own_numbers = convert_to_int_list(own_numbers_section.strip().split(" "))
            scratch_cards.append((winning_numbers, own_numbers))
    return scratch_cards


def solve_01(data: list[tuple[list[int], list[int]]]) -> int:
    # variables initialization
    total_points = 0
    for winning, own in data:
        matches = 0
        for number in own:
            if number in winning:
                matches += 1
        if matches:
            total_points += pow(2, matches - 1)

    return total_points


def main() -> None:
    # input.txt | example_1.txt
    data = parse_input(INPUT_FILE_PATH / "example_1.txt")
    solution = solve_01(data)
    print(f"The solution of the example is {solution}")
    data = parse_input(INPUT_FILE_PATH / "input.txt")
    solution = solve_01(data)
    print(f"The solution of part 1 is {solution}")


if __name__ == "__main__":
    main()
