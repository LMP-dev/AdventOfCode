from pathlib import Path
import re
import time

INPUT_FILE = Path(__file__).parent / "input.txt"
ROW_TO_STUDY = 2000000
# INPUT_FILE = Path(__file__).parent / "test_input.txt"
# ROW_TO_STUDY = 10


class Sensor:
    def __init__(self, x: int, y: int, beacon_x: int, beacon_y: int) -> None:
        self.x = x
        self.y = y
        self.beacon = (beacon_x, beacon_y)

    @property
    def manhatan_dis(self):
        return abs(self.x - self.beacon[0]) + abs(self.y - self.beacon[1])

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
        points = list()
        # num of points inside manhatthan range at that row (piramid formula)
        num_points = self._range_points_in_row(row)
        # Calculate coordinates of points at that row
        central_point = (row, self.y)
        points.append(central_point)
        for i in range((num_points - 1) // 2):
            left_side_point = (row, self.y - 1 - i)
            right_side_point = (row, self.y + 1 + i)
            points.append(left_side_point)
            points.append(right_side_point)
        return points


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


def main() -> None:
    # Parse sensors and becons
    sensors = create_sensors(INPUT_FILE)
    # Collect manhattan ranges (only the ones affecting the row)
    manhatan_ranges = list()
    sensors_pos = list()
    beacons_pos = set()
    for sensor in sensors:
        # Calculate manhattan range
        if sensor.row_in_manhattan_range(ROW_TO_STUDY):
            manhatan_ranges.extend(sensor.manhattan_range_at_row(ROW_TO_STUDY))
        # Update positions list
        sensors_pos.append((sensor.x, sensor.y))
        beacons_pos.update({(sensor.beacon)})
    # Sort ranges and only collect the desired row
    unique_ranges = set(manhatan_ranges)
    cannot_contain_beacon = list()
    for pos in unique_ranges:
        if pos in sensors_pos or pos in beacons_pos:
            pass
        else:
            cannot_contain_beacon.append(pos)
    print(len(cannot_contain_beacon))


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"--- {time.time() - start} seconds ---")
