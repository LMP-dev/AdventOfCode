"""
3 different possibilities allowed:
    - No arguments passed (the script will ask for them later)
    - only 1 argument passed: day. The script will use the current year as year
    - day and year passed (in this order: day | year)
"""

# Standard library
from pathlib import Path
import sys
from datetime import datetime
import requests

# 3rd party library
from jinja2 import Environment, FileSystemLoader

REPO_PATH = Path(__file__).parent
TEMPLATE_PATH = REPO_PATH / "templates"

PUZZLE_TEMPLATE_FILENAME = "main.txt"
FIRST_PUZZLE_NAME = "PuzzleA.py"
EXAMPLE_NAME = "example_1.txt"
PUZZLE_INPUT_FILENAME = "input.txt"
SESSION_ID_FILE = "session.cookie"  # Make sure you have created this file (is in .gitignore to avoid security breaches)


def create_puzzle_folder(year: str, day: str) -> Path:
    """Creates the year folder (if does not exists) and then the day folder"""
    Path(REPO_PATH / year).mkdir(exist_ok=True)
    try:
        puzzle_path = REPO_PATH / year / f"day_{int(day):02d}"
        puzzle_path.mkdir()
    except FileExistsError:
        raise Exception(
            f"You have already a directory for the day {day} of the year {year}"
        )
    return puzzle_path


def create_puzzle_template_file_content(part: str) -> str:
    environment = Environment(loader=FileSystemLoader(TEMPLATE_PATH))
    template = environment.get_template(PUZZLE_TEMPLATE_FILENAME)
    content = template.render(part=part)

    return content


def parse_system_arguments() -> tuple[str | None, str | None]:
    """return (day, year)"""
    arguments = sys.argv[1:]
    if len(arguments) == 0:
        return None, None
    if len(arguments) == 1:
        day: str = arguments[0]
        if len(day) in [1, 2]:
            return day, str(datetime.now().year)
        else:
            raise Exception(
                f"Remember the first argument are the days. Use a correct format (1 or 2 digits). You inputed: {day}"
            )
    if len(arguments) == 2:
        day, year = arguments
        if len(day in [1, 2]) and len(year == 4):
            return day, year
        else:
            raise Exception(
                "Please review the arguments inputed. The order is: day | year"
            )
    else:
        raise Exception(
            "Please do not define more than 2 arguments in total: day | year"
        )


def store_file(file_path: Path, content="") -> None:
    with open(file_path, "w") as file:
        file.write(content)


def get_url(year: int, day: int):
    return f"https://adventofcode.com/{year}/day/{day}/input"


def get_session_id(cookie_file: Path) -> str:
    with open(cookie_file) as file:
        return file.read().strip()


def download_problem_data(day: int, year: int, path_to_save: Path) -> None:
    # Create url and session inputs
    url = get_url(int(year), int(day))
    cookies = {"session": get_session_id(SESSION_ID_FILE)}

    # Connect to Advent of Code website
    response = requests.get(url, cookies=cookies)
    if not response.ok:
        raise RuntimeError(
            f"Request failed\n\tstatus code: {response.status_code}\n\tmessage: {response.content}"
        )

    # Store input file
    with open(path_to_save, "w") as file:
        file.write(response.text[:-1])


def main() -> None:
    # Read arguments or ask for inputs:
    day, year = parse_system_arguments()  # format is str
    if year is None:
        year = input("Which year do you want to do (format yyyy)?\n")
    if day is None:
        day = input("Which day do you want to solve (format d or dd)?\n")

    # Create main.py template content
    content = create_puzzle_template_file_content(part=1)

    # Create folders
    puzzle_path = create_puzzle_folder(year, day)

    # Create files
    store_file(puzzle_path / FIRST_PUZZLE_NAME, content=content)
    store_file(puzzle_path / EXAMPLE_NAME)

    # Download problem data
    download_problem_data(int(day), int(year), puzzle_path / PUZZLE_INPUT_FILENAME)

    # Create testing folders and templates
    # TODO


if __name__ == "__main__":
    main()
