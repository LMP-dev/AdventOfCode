from pathlib import Path
from dataclasses import dataclass

INPUT_FILE = Path(__file__).parent / "input.txt"

@dataclass
class Top3Elves:
    top_1: int
    top_2: int
    top_3: int

    @property
    def total_cal(self) -> int:
        return self.top_1 + self.top_2 + self.top_3

def compare_top_3(top_elves: Top3Elves, value: int) -> Top3Elves:    
    if value > top_elves.top_1:
        return Top3Elves(value, top_elves.top_1, top_elves.top_2)
    elif value > top_elves.top_2:
        return Top3Elves(top_elves.top_1, value, top_elves.top_3)
    elif value > top_elves.top_3:
        return Top3Elves(top_elves.top_1, top_elves.top_2, value)
    return top_elves


def main() -> None:
    top_elves = Top3Elves(0,0,0)
    with open(INPUT_FILE, 'r') as file:
        elf_pack_cal = 0
        for line in file:
            if line.strip():
                elf_pack_cal += int(line)
            else:
                top_elves = compare_top_3(top_elves, elf_pack_cal)
                elf_pack_cal = 0
    
    print(top_elves.total_cal)

if __name__ == "__main__":
    main()
