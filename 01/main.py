from pathlib import Path

INPUT_FILE = Path(__file__).parent / "input.txt"

def main() -> None:
    most_cal = 0
    with open(INPUT_FILE, 'r') as file:
        elf_pack_cal = 0
        for line in file:
            if line.strip():
                elf_pack_cal += int(line)
            else:
                if elf_pack_cal > most_cal:
                    most_cal = elf_pack_cal
                elf_pack_cal = 0
    
    print(most_cal)

if __name__ == "__main__":
    main()
