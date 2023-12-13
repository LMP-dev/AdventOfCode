# Standard library
import itertools
from pathlib import Path

INPUT_FILE_PATH = Path(__file__).parent


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def parse_input(file_content: list[str]) -> list[list[int]]:
    values_history = []
    for content in file_content:
        values = content.split(" ")
        value_history = [int(val) for val in values]
        values_history.append(value_history)
    return values_history


def find_extrapolation_data(history_val: list[int], first_val: list) -> list[int]:
    """Last values of each row is stored in list last_val"""
    diff_values = [y - x for x, y in zip(history_val[:-1], history_val[1:])]
    first_val.append(history_val[0])

    all_same_value = diff_values.count(diff_values[0]) == len(diff_values)
    if all_same_value and diff_values[0] == 0:
        first_val.append(0)
        return first_val
    else:
        return find_extrapolation_data(diff_values, first_val)


def solve_01(data: list[list[int]]) -> int:
    values_histories = 0

    for history in data:
        extrapolation_data = find_extrapolation_data(history, [])
        extrapolation_data.reverse()
        prediction_value = 0
        for value in extrapolation_data:
            prediction_value = value - prediction_value
        values_histories += prediction_value

    return values_histories


def main() -> None:
    # input.txt | example_1.txt | example_1_v2.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of the example 1 is {solution}")
    file_content = read_data(INPUT_FILE_PATH / "input.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of the part 2 is {solution}")


if __name__ == "__main__":
    main()
