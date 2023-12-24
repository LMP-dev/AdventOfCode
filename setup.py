# Standard library
from pathlib import Path

# 3rd party library
from jinja2 import Environment, FileSystemLoader

REPO_PATH = Path(__file__).parent
TEMPLATE_PATH = REPO_PATH / "templates"

PUZZLE_TEMPLATE_FILENAME = "main.txt"


def create_puzzle_folder() -> None:
    return


def create_puzzle_template_file_content(part: str) -> str:
    environment = Environment(loader=FileSystemLoader(TEMPLATE_PATH))
    template = environment.get_template(PUZZLE_TEMPLATE_FILENAME)
    content = template.render(part=part)

    return content


# Create new folder (check if already created)

# Create template problem

part = input("Which puzzle part are you doing(1 or 2)?\n")
content = create_puzzle_template_file_content(part)

# Create testing template

# Download problem data
