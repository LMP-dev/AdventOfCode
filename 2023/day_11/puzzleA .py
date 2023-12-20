# Standard library
from pathlib import Path

INPUT_FILE_PATH = Path(__file__).parent


def read_data(
    file_path: Path,
) -> list[str]:
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return lines


def parse_input(file_content: list[str]) -> list[list[str]]:
    grid: list[list[str]] = []
    for line in file_content:
        # Parse lines and add extra expanded rows when all "."
        row = list(line)
        if row.count(".") == len(row):
            grid.append(row)
        grid.append(row)

    # Expand columns
    ...

    return


def solve_01(data: tuple[list[list[str]], tuple[int, int]]) -> int:
    step = 0
    # create all pairs

    # find distances by coordinates

    return step


def main() -> None:
    # input.txt | example_1.txt | example_1_v2.txt
    file_content = read_data(INPUT_FILE_PATH / "example_1.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of the example 1 is {solution}")
    file_content = read_data(INPUT_FILE_PATH / "input.txt")
    data = parse_input(file_content)
    solution = solve_01(data)
    print(f"The solution of the part 1 is {solution}")


if __name__ == "__main__":
    main()
