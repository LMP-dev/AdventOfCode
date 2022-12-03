from pathlib import Path
from itertools import islice

INPUT_FILE = Path(__file__).parent / "input.txt"

def find_batch(elf_group: list[str]) -> str:
    pack_1, pack_2, pack_3 = elf_group
    for char in pack_1:
        if char in pack_2:
            if char in pack_3:
                return char

def calculate_prio(char: str) -> int:
    if char.islower():
        return ord(char) - 96
    elif char.isupper():
        return ord(char) - 38

def main() -> None:
    prios_sum = 0
    with open(INPUT_FILE, 'r') as file:
        while True:
            elf_group = list(islice(file, 3))
            if not elf_group:
                break
            badge = find_batch(elf_group)
            prios_sum += calculate_prio(badge)
    print(prios_sum)

if __name__ == "__main__":
    main()
