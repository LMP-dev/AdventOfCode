from pathlib import Path

INPUT_FILE = Path(__file__).parent / "input.txt"

def split_str_in_half(line: str) -> tuple[str]:
    first_half = line[:len(line)//2]
    second_half = line[len(line)//2:]
    return first_half, second_half

def calculate_prio(char: str) -> int:
    if char.islower():
        return ord(char) - 96
    elif char.isupper():
        return ord(char) - 38

def main() -> None:
    prios_sum = 0
    with open(INPUT_FILE, 'r') as file:
        for line in file:
            comp_1, comp_2 = split_str_in_half(line)
            for char in comp_1:
                if char in comp_2:
                    prios_sum += calculate_prio(char)
                    break
    print(prios_sum)

if __name__ == "__main__":
    main()
