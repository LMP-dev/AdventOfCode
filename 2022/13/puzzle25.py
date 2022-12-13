from pathlib import Path

INPUT_FILE = Path(__file__).parent / "input.txt"
# INPUT_FILE = Path(__file__).parent / "test_input.txt"


def compare_packet_data(pack_1: list[list | int], pack_2: list[list | int]) -> bool:
    for i, j in zip(pack_1, pack_2):
        if isinstance(i, int):
            if isinstance(j, int):
                # int vs int
                if i < j:
                    return True
                elif i == j:
                    continue
                else:
                    return False
            else:
                # int vs list
                comparison = compare_packet_data([i], j)
                if comparison is None:
                    continue
                else:
                    return comparison
        else:
            if isinstance(j, int):
                # list vs int
                comparison = compare_packet_data(i, [j])
                if comparison is None:
                    continue
                else:
                    return comparison
            else:
                comparison = compare_packet_data(i, j)
                if comparison is None:
                    continue
                else:
                    return comparison

    if len(pack_1) > len(pack_2):
        return False
    elif len(pack_1) < len(pack_2):
        return True
    else:
        return None


def main() -> None:
    indexes = list()
    with open(INPUT_FILE, "r") as file:
        index = 1
        for line in file:
            if not line.strip():
                continue
            other_line = next(file)
            packet_pair_1 = eval(line)
            packet_pair_2 = eval(other_line)
            equal = compare_packet_data(packet_pair_1, packet_pair_2)
            if equal:
                indexes.append(index)
            index += 1

    print(sum(indexes))


if __name__ == "__main__":
    main()
