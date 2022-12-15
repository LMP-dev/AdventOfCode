from pathlib import Path
import re
import time

INPUT_FILE = Path(__file__).parent / "input.txt"
# INPUT_FILE = Path(__file__).parent / "test_input.txt"


class Sensor:
    def __init__(self, x: int, y: int, beacon_x: int, beacon_y: int) -> None:
        self.x = x
        self.y = y
        self.beacon = (beacon_x, beacon_y)
        self.manhatan_dis = abs(self.x - self.beacon[0]) + abs(self.y - self.beacon[1])

    def row_in_manhattan_range(self, row: int) -> bool:
        if row >= self.x - self.manhatan_dis and row <= self.x + self.manhatan_dis:
            return True
        return False

    def _range_points_in_row(self, row: int) -> int:
        if row >= self.x and row <= self.x + self.manhatan_dis:
            # Lower triangle
            return 1 + 2 * (self.x + self.manhatan_dis - row)
        else:
            # Upper triangle
            return 1 + 2 * abs(self.x - self.manhatan_dis - row)

    def manhattan_range_at_row(self, row: int) -> list[tuple]:
        # num of points inside manhatthan range at that row (piramid formula)
        num_points = self._range_points_in_row(row)
        # Calculate start and end columns
        range_sensor = (self.y - num_points // 2, self.y + num_points // 2)
        return range_sensor


def create_sensors(file_path: Path) -> tuple[list[Sensor]]:
    """Returns a list of sensors and the min and max columns"""
    sensors = list()
    with open(file_path, "r") as file:
        for line in file:
            numbers = re.findall("([-]*[0-9]+)", line)
            sensor = Sensor(
                int(numbers[1]), int(numbers[0]), int(numbers[3]), int(numbers[2])
            )
            sensors.append(sensor)
    return sensors


def calculate_row_occupacy(sensors: list[Sensor], row: int) -> set[tuple[int]]:
    manhatan_ranges = list()
    for sensor in sensors:
        # Calculate manhattan range
        if sensor.row_in_manhattan_range(row):
            manhatan_ranges.append(sensor.manhattan_range_at_row(row))
    return manhatan_ranges


def merge_overlaping_ranges(ranges: list[tuple[int]]) -> list[tuple]:
    """
    Merges a list of ranges [(a,b), (c,d), (e,f), ...]
    Rules:
    #================================================
    # b+1<c: a-----b              Ans: [(a,b),(c,d)]
    #                 c---d
    # c<=b+1 and b<d: a-----b     Ans: [(a,d)]
    #                     c---d
    # c < b and d<=b: a-----b     Ans: [(a,b)]
    #                  c---d
    #================================================
    """
    sorted_ranges = sorted(ranges)
    final_ranges = [sorted_ranges[0]]
    for c, d in sorted_ranges[1:]:
        a, b = final_ranges[-1]

        if b + 1 < c:
            final_ranges.append((c, d))
        elif b <= d:
            final_ranges[-1] = (a, d)
        else:
            pass
    return final_ranges


def tuning_frequency(row: int, column: int) -> int:
    return column * 4000000 + row


def main() -> None:
    max_val = 4000000
    # Parse sensors and becons
    sensors = create_sensors(INPUT_FILE)
    # Collect manhattan ranges (only the ones affecting the row)
    for i in range(max_val + 1):
        manhatan_ranges = calculate_row_occupacy(sensors, i)
        merged = merge_overlaping_ranges(manhatan_ranges)
        if len(merged) > 1:
            row = i
            ranges = merged
            break
    col = ranges[0][1] + 1
    print(tuning_frequency(row, col))


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"--- {time.time() - start} seconds ---")
