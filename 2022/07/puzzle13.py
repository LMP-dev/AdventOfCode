from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass
import re

INPUT_FILE = Path(__file__).parent / "input.txt"
# INPUT_FILE = Path(__file__).parent / "test_input.txt"
PATTERN_FILE = re.compile(r"(\d+)\s+(\w+)")
PATTERN_FOLDER = re.compile(r"\w+\s+(\w+)")


@dataclass
class File:
    name: str
    size: int

    def __hash__(self):
        return hash((self.name, self.size))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.name == other.name and self.size == other.size


class Directory:
    def __init__(self, name: str, parent: Directory = None) -> None:
        self.name = name
        self.parent = parent
        self.childs = set()
        self.files = set()
        self.size = None

    def add_directory(self, directory: Directory) -> None:
        self.childs.update([directory])

    def add_file(self, file: File) -> None:
        self.files.update([file])

    def _calculate_sizes(self) -> int:
        if self.size:
            return self.size

        _total_size = 0
        for file in self.files:
            _total_size += file.size
        for dir in self.childs:
            if dir.size:
                _total_size += dir.size
            else:
                _total_size += dir._calculate_sizes()
        self.size = _total_size
        return _total_size


def create_file_tree(input_file: Path) -> Directory:
    root_dir = None
    with open(input_file, "r") as file:
        cwd = None
        for line in file:
            if line.startswith("$ cd "):
                folder = line[5:].strip()
                # Check special case ..
                if folder == "..":
                    cwd = cwd.parent
                    continue
                dir = Directory(folder, parent=cwd)
                if not cwd:
                    root_dir = dir
                else:
                    cwd.add_directory(dir)
                cwd = dir
            elif line.startswith("$ ls"):
                pass
            else:
                match_file = PATTERN_FILE.match(line)
                if match_file:
                    size, name = match_file.groups()
                    cwd.add_file(File(name.strip(), int(size)))

    return root_dir


def calculate_sum_folders(
    sum_dir: list[int], folder: Directory, max_size: int
) -> list[int]:
    if folder.size <= max_size:
        sum_dir.append(folder.size)
    if not folder.childs:
        return sum_dir
    else:
        for subfolder in folder.childs:
            sum_dir = calculate_sum_folders(sum_dir, subfolder, max_size)
        return sum_dir


def main() -> None:
    root_dir = create_file_tree(INPUT_FILE)
    root_dir._calculate_sizes()
    folders_under_max = calculate_sum_folders(list(), root_dir, 100000)
    print(sum(folders_under_max))


if __name__ == "__main__":
    main()
