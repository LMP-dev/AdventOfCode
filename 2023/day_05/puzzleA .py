from pathlib import Path
from dataclasses import dataclass
import math

INPUT_FILE_PATH = Path(__file__).parent


@dataclass
class MappingSet:
    dest_range: int
    source_range: int
    range_lenght: int

    def in_range(self, number: int) -> bool:
        if self.source_range <= number <= self.source_range + self.range_lenght - 1:
            return True
        return False

    def convert(self, number: int) -> int:
        """Assume the number is in range. Use before the in_range method to check!"""
        diff = number - self.source_range
        return self.dest_range + diff


class Mapper:
    def __init__(self) -> None:
        self.mapping_sets: list[MappingSet] = []

    def add_mapping_set(self, mapping_set: MappingSet) -> None:
        self.mapping_sets.append(mapping_set)

    def map(self, number: int) -> int:
        for mapping_set in self.mapping_sets:
            if mapping_set.in_range(number):
                return mapping_set.convert(number)
        return number


class LocationFinder:
    def __init__(self, mappers: list[Mapper]) -> None:
        self.mappers = mappers

    def get_location(self, seed: int) -> int:
        current_value = seed
        for map in self.mappers:
            current_value = map.map(current_value)
        return current_value


def parse_input(
    file_path: Path,
) -> tuple[list[int], LocationFinder]:
    # parse_input
    seeds: list[int] = []

    seed_to_soil_map = Mapper()
    soil_to_fertilizer_map = Mapper()
    fertilizer_to_water_map = Mapper()
    water_to_light_map = Mapper()
    light_to_temperature_map = Mapper()
    temperature_to_humidity_map = Mapper()
    humidity_to_location_map = Mapper()

    with open(file_path) as file:
        print(f"------ OPENED FILE!")
        # Initialize flags for parsing
        inside_seed_to_soil = False
        inside_soil_to_fertilizer = False
        inside_fertilizer_to_water = False
        inside_water_to_light = False
        inside_light_to_temperature = False
        inside_temperature_to_humidity = False
        inside_humidity_to_location = False

        for raw_line in file:
            line = raw_line.strip()
            # Parse first line with seed numbers
            if line.startswith("seeds"):
                _, seed_numbers_section = line.split(":")
                seed_numbers_str = seed_numbers_section.strip().split(" ")
                seeds = [int(seed_num) for seed_num in seed_numbers_str]
            # Parse seed-to-soil map
            elif line.startswith("seed-to-soil"):
                inside_seed_to_soil = True
                print(f"------ FOUND line correpsonding to seed-to-soil")
            elif inside_seed_to_soil:
                if not line:
                    inside_seed_to_soil = False
                    continue
                dest_range_str, source_range_str, range_length_str = line.split(" ")
                seed_to_soil_map.add_mapping_set(
                    MappingSet(
                        int(dest_range_str),
                        int(source_range_str),
                        int(range_length_str),
                    )
                )
            # Parse soil-to-fertilizer map
            elif line.startswith("soil-to-fertilizer"):
                inside_soil_to_fertilizer = True
                print(f"------ FOUND line correpsonding to soil-to-fertilizer")
            elif inside_soil_to_fertilizer:
                if not line:  # Detects empty line separating maps
                    inside_soil_to_fertilizer = False
                    continue
                dest_range_str, source_range_str, range_length_str = line.split(" ")
                soil_to_fertilizer_map.add_mapping_set(
                    MappingSet(
                        int(dest_range_str),
                        int(source_range_str),
                        int(range_length_str),
                    )
                )
            # Parse fertilizer-to-water map
            elif line.startswith("fertilizer-to-water"):
                inside_fertilizer_to_water = True
                print(f"------ FOUND line correpsonding to fertilizer-to-water")
            elif inside_fertilizer_to_water:
                if not line:
                    inside_fertilizer_to_water = False
                    continue
                dest_range_str, source_range_str, range_length_str = line.split(" ")
                fertilizer_to_water_map.add_mapping_set(
                    MappingSet(
                        int(dest_range_str),
                        int(source_range_str),
                        int(range_length_str),
                    )
                )
            # Parse water-to-light map
            elif line.startswith("water-to-light"):
                inside_water_to_light = True
                print(f"------ FOUND line correpsonding to water-to-light")
            elif inside_water_to_light:
                if not line:
                    inside_water_to_light = False
                    continue
                dest_range_str, source_range_str, range_length_str = line.split(" ")
                water_to_light_map.add_mapping_set(
                    MappingSet(
                        int(dest_range_str),
                        int(source_range_str),
                        int(range_length_str),
                    )
                )
            # Parse light-to-temperature map
            elif line.startswith("light-to-temperature"):
                inside_light_to_temperature = True
                print(f"------ FOUND line correpsonding to light-to-temperature")
            elif inside_light_to_temperature:
                if not line:
                    inside_light_to_temperature = False
                    continue
                dest_range_str, source_range_str, range_length_str = line.split(" ")
                light_to_temperature_map.add_mapping_set(
                    MappingSet(
                        int(dest_range_str),
                        int(source_range_str),
                        int(range_length_str),
                    )
                )
            # Parse temperature-to-humidity map
            elif line.startswith("temperature-to-humidity"):
                inside_temperature_to_humidity = True
                print(f"------ FOUND line correpsonding to temperature-to-humidity")
            elif inside_temperature_to_humidity:
                if not line:
                    inside_temperature_to_humidity = False
                    continue
                dest_range_str, source_range_str, range_length_str = line.split(" ")
                temperature_to_humidity_map.add_mapping_set(
                    MappingSet(
                        int(dest_range_str),
                        int(source_range_str),
                        int(range_length_str),
                    )
                )
            # Parse humidity-to-location map
            elif line.startswith("humidity-to-location"):
                inside_humidity_to_location = True
                print(f"------ FOUND line correpsonding to humidity-to-location")
            elif inside_humidity_to_location:
                if not line:
                    inside_humidity_to_location = False
                    continue
                dest_range_str, source_range_str, range_length_str = line.split(" ")
                humidity_to_location_map.add_mapping_set(
                    MappingSet(
                        int(dest_range_str),
                        int(source_range_str),
                        int(range_length_str),
                    )
                )

    location_finder = LocationFinder(
        [
            seed_to_soil_map,
            soil_to_fertilizer_map,
            fertilizer_to_water_map,
            water_to_light_map,
            light_to_temperature_map,
            temperature_to_humidity_map,
            humidity_to_location_map,
        ]
    )

    return seeds, location_finder


def solve_01(data: list[int]) -> int:
    seeds, finder = data
    # variables initialization
    minimum_location = math.inf
    for seed in seeds:
        location = finder.get_location(seed)
        minimum_location = min(minimum_location, location)
        print(f"FINISHED MAPPING for seed: {seed}")

    return minimum_location


def main() -> None:
    # input.txt | example_1.txt
    data = parse_input(INPUT_FILE_PATH / "example_1.txt")
    solution = solve_01(data)
    print(f"The solution of the example is {solution}")
    data = parse_input(INPUT_FILE_PATH / "input.txt")
    solution = solve_01(data)  # 25004
    print(f"The solution of part 1 is {solution}")


if __name__ == "__main__":
    main()
