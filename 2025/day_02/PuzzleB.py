# Standard library
from pathlib import Path
import math

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


def divisors_without_1(num: int) -> set[int]:
    """Calculates all the divisors of the number without considering 1"""
    divisors: set[int] = set()
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            divisors.add(i)
            divisors.add(num // i)
    divisors.add(num)
    return divisors


def is_bad_id(num: int) -> bool:
    # Convert back to string
    num_str = str(num)

    number_size = len(num_str)
    # Single digits should not be considered
    if number_size == 1:
        return False

    divisors_length = divisors_without_1(number_size)

    for size in divisors_length:
        # Split string in x parts
        chunk_size = number_size // size
        number_parts = [
            int(num_str[i * chunk_size : (i + 1) * chunk_size]) for i in range(size)
        ]
        # Check if all parts are equal
        if all(x == number_parts[0] for x in number_parts):
            return True

    return False


def solve_02(data: list[tuple[int, int]]) -> int:
    invalid_ids: list[int] = []

    for min_id, max_id in data:
        for id in range(min_id, max_id + 1):  # +1 to end in the number
            if is_bad_id(id):
                # print(f"In range ({min_id}, {max_id}) the number {id} is invalid")
                invalid_ids.append(id)

    return sum(invalid_ids)


def main() -> None:
    # input.txt | example_1.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_02(data)
    print(f"The solution of the example 1 is {solution}")
    file_content = read_data(INPUT_FILE_PATH / "input.txt")
    data = parse_input(file_content)
    solution = solve_02(data)
    print(f"The solution of the part 2 is {solution}")


if __name__ == "__main__":
    main()
