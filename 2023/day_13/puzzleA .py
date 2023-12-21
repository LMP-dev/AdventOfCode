# Standard library
from pathlib import Path

INPUT_FILE_PATH = Path(__file__).parent


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def parse_input(file_content: list[str]) -> list[list[list[str]]]:
    patterns = []
    pattern = []
    for line in file_content:
        if line:
            pattern.append(list(line))
        else:
            patterns.append(pattern)
            pattern = list()
    patterns.append(pattern)
    return patterns


def solve_01(data: list[list[list[str]]]) -> int:
    return


def main() -> None:
    # input.txt | example_1.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of the example 1 is {solution}")
    # file_content = read_data(INPUT_FILE_PATH / "input.txt")
    # data = parse_input(file_content)
    # solution = solve_01(data)
    # print(f"The solution of the part 1 is {solution}")


if __name__ == "__main__":
    main()
