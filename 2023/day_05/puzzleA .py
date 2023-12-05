from pathlib import Path
import math

INPUT_FILE_PATH = Path(__file__).parent


def parse_input(
    file_path: Path,
) -> tuple[list[tuple[list[int], list[int]]], list[dict[int, int]]]:
    # Utility function
    def fill_dictionary_with_ranges(
        selected_dict: dict[int, int],
        dest_range: int,
        source_range: int,
        range_lenght: int,
    ) -> dict[int, int]:
        for i in range(range_lenght):
            selected_dict.update({source_range + i: dest_range + i})
        return selected_dict

    # parse_input
    seeds: list[int] = []

    seed_to_soil_map = {}
    soil_to_fertilizer_map = {}
    fertilizer_to_water_map = {}
    water_to_light_map = {}
    light_to_temperature_map = {}
    temperature_to_humidity_map = {}
    humidity_to_location_map = {}

    with open(file_path) as file:
        for raw_line in file:
            # Initialize flags for parsing
            inside_seed_to_soil = False
            inside_soil_to_fertilizer = False
            inside_fertilizer_to_water = False
            inside_water_to_light = False
            inside_light_to_temperature = False
            inside_temperature_to_humidity = False
            inside_humidity_to_location = False

            line = raw_line.strip()
            # Parse first line with seed numbers
            if line.startswith("seeds"):
                _, seed_numbers_section = line.split(":")
                seed_numbers_str = seed_numbers_section.strip().split(" ")
                seeds = [int(seed_num) for seed_num in seed_numbers_str]
            # Parse seed-to-soil map
            elif line.startswith("seed-to-soil"):
                inside_seed_to_soil = True
            elif inside_seed_to_soil:
                dest_range_str, source_range_str, range_length_str = line.split(" ")
                seed_to_soil_map = fill_dictionary_with_ranges(
                    seed_to_soil_map,
                    int(dest_range_str),
                    int(source_range_str),
                    int(range_length_str),
                )
            # Parse soil-to-fertilizer map
            elif line.startswith("soil-to-fertilizer"):
                inside_soil_to_fertilizer = True
            elif inside_soil_to_fertilizer:
                dest_range_str, source_range_str, range_length_str = line.split(" ")
                soil_to_fertilizer_map = fill_dictionary_with_ranges(
                    soil_to_fertilizer_map,
                    int(dest_range_str),
                    int(source_range_str),
                    int(range_length_str),
                )
            # Parse fertilizer-to-water map
            elif line.startswith("fertilizer-to-water"):
                inside_fertilizer_to_water = True
            elif inside_fertilizer_to_water:
                dest_range_str, source_range_str, range_length_str = line.split(" ")
                fertilizer_to_water_map = fill_dictionary_with_ranges(
                    fertilizer_to_water_map,
                    int(dest_range_str),
                    int(source_range_str),
                    int(range_length_str),
                )
            # Parse water-to-light map
            elif line.startswith("water-to-light"):
                inside_water_to_light = True
            elif inside_water_to_light:
                dest_range_str, source_range_str, range_length_str = line.split(" ")
                water_to_light_map = fill_dictionary_with_ranges(
                    water_to_light_map,
                    int(dest_range_str),
                    int(source_range_str),
                    int(range_length_str),
                )
            # Parse light-to-temperature map
            elif line.startswith("light-to-temperature"):
                inside_light_to_temperature = True
            elif inside_light_to_temperature:
                dest_range_str, source_range_str, range_length_str = line.split(" ")
                light_to_temperature_map = fill_dictionary_with_ranges(
                    light_to_temperature_map,
                    int(dest_range_str),
                    int(source_range_str),
                    int(range_length_str),
                )
            # Parse temperature-to-humidity map
            elif line.startswith("temperature-to-humidity"):
                inside_temperature_to_humidity = True
            elif inside_temperature_to_humidity:
                dest_range_str, source_range_str, range_length_str = line.split(" ")
                temperature_to_humidity_map = fill_dictionary_with_ranges(
                    temperature_to_humidity_map,
                    int(dest_range_str),
                    int(source_range_str),
                    int(range_length_str),
                )
            # Parse humidity-to-location map
            elif line.startswith("humidity-to-location"):
                inside_humidity_to_location = True
            elif inside_humidity_to_location:
                dest_range_str, source_range_str, range_length_str = line.split(" ")
                humidity_to_location_map = fill_dictionary_with_ranges(
                    humidity_to_location_map,
                    int(dest_range_str),
                    int(source_range_str),
                    int(range_length_str),
                )

            else:
                # Reset flags
                inside_seed_to_soil = False
                inside_soil_to_fertilizer = False
                inside_fertilizer_to_water = False
                inside_water_to_light = False
                inside_light_to_temperature = False
                inside_temperature_to_humidity = False
                inside_humidity_to_location = False

    map_list = [
        seed_to_soil_map,
        soil_to_fertilizer_map,
        fertilizer_to_water_map,
        water_to_light_map,
        light_to_temperature_map,
        temperature_to_humidity_map,
        humidity_to_location_map,
    ]

    return seeds, map_list


def solve_01(data: list[int]) -> int:
    seeds, map_list = data

    # variables initialization
    minimum_location = math.inf

    for seed in seeds:
        current = seed
        # Transform with maps until location
        for map in map_list:
            try:
                current = map[current]
            except KeyError:
                pass  # current = current
        minimum_location = min(minimum_location, current)

    return minimum_location


def main() -> None:
    # input.txt | example_1.txt
    data = parse_input(INPUT_FILE_PATH / "example_1.txt")

    print(f"seed_to_soil_map: {data[1][0]}")
    print(f"soil_to_fertilizer_map: {data[1][1]}")
    print(f"fertilizer_to_water_map: {data[1][2]}")
    print(f"water_to_light_map: {data[1][3]}")
    print(f"light_to_temperature_map: {data[1][4]}")
    print(f"temperature_to_humidity_map: {data[1][5]}")
    print(f"humidity_to_location_map: {data[1][6]}")

    solution = solve_01(data)
    print(f"The solution of the example is {solution}")
    # data = parse_input(INPUT_FILE_PATH / "input.txt")
    # solution = solve_01(data)  # 25004
    # print(f"The solution of part 1 is {solution}")


if __name__ == "__main__":
    main()
