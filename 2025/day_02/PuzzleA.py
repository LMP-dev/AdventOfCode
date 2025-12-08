# Standard library
from pathlib import Path

INPUT_FILE_PATH = Path(__file__).parent


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def parse_input(file_content: list[str]) -> list[tuple[int, int]]:
    input_line = file_content[0]
    range_list = input_line.split(",")

    return [map(int, item.split("-")) for item in range_list]


def is_bad_id(num: int) -> bool:
    # Convert back to string
    num_str = str(num)

    half_size, rem = divmod(len(num_str), 2)
    # Avoid odd combinations of characters
    if rem != 0:
        return False
    first_half = num_str[:half_size]
    second_half = num_str[half_size:]

    # Check equal half
    if int(first_half) == int(second_half):
        return True

    return False


def solve_01(data: list[tuple[int, int]]) -> int:
    invalid_ids: list[int] = []

    for min_id, max_id in data:
        for id in range(min_id, max_id + 1):  # +1 to end in the number
            if is_bad_id(id):
                invalid_ids.append(id)

    return sum(invalid_ids)


def main() -> None:
    # input.txt | example_1.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of the example 1 is {solution}")  # Solution 1227775554
    file_content = read_data(INPUT_FILE_PATH / "input.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of the part 1 is {solution}")  # Solution 41294979841


if __name__ == "__main__":
    main()
