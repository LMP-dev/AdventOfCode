from pathlib import Path
import itertools
from typing import Iterator

INPUT_FILE = Path(__file__).parent / "input.txt"
# INPUT_FILE = Path(__file__).parent / "test_input.txt"
divider_packet_1 = [[2]]
divider_packet_2 = [[6]]


def flatten_list(packet: list[list | int]) -> Iterator:
    try:
        if len(packet) == 0:
            yield -1
    except TypeError:
        pass

    for item in packet:
        try:
            yield from flatten_list(item)
        except TypeError:
            yield item


def flaten(_list: list[list | int]) -> list[int]:
    return list(flatten_list(_list))


def main() -> None:
    with open(INPUT_FILE, "r") as file:
        distress_signal = list()
        flaten_distress = list()
        for line in file:
            if not line.strip():
                continue
            packet = eval(line.strip())
            distress_signal.append(packet)
            flaten_distress.append(flaten(packet))

    distress_signal.append(divider_packet_1)
    distress_signal.append(divider_packet_2)
    ordered_signal = sorted(distress_signal, key=flaten)
    index_1 = ordered_signal.index(divider_packet_1) + 1
    index_2 = ordered_signal.index(divider_packet_2) + 1
    print(index_1 * index_2)


if __name__ == "__main__":
    main()
