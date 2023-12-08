from functools import reduce
from numpy import lcm

OUTPUT_TYPE = int


def parse_inp(inp: list[str]) -> tuple[str, dict[str, tuple[str, str]]]:
    directions: str = inp[0].strip()
    paths: dict[str, tuple[str, str]] = {}
    for path in inp[2:]:
        path = path.replace("\n", "")
        path_split: list[str] = path.split(" ")
        paths[path_split[0]] = (path_split[2][1:-1], path_split[3][:-1])
    return directions, paths


def main_part_1(inp: list[str]) -> OUTPUT_TYPE:
    directions: str
    paths: dict[str, tuple[str, str]]
    directions, paths = parse_inp(inp)
    location: str = "AAA"
    steps: int = 0
    while location != "ZZZ":
        location = paths[location]["LR".index(
            directions[steps % len(directions)])]
        steps += 1
    return steps


def main_part_2(inp: list[str]) -> OUTPUT_TYPE:
    directions: str
    paths: dict[str, tuple[str, str]]
    directions, paths = parse_inp(inp)

    locations: list[str] = [
        location
        for location in paths.keys()
        if location.endswith("A")
    ]
    start: list[str] = locations.copy()
    periods: list[int] = [-1 for _ in start]
    steps: int = 0

    while True:
        locations = [
            paths[location]["LR".index(directions[steps % len(directions)])]
            for location in locations
        ]
        steps += 1

        for index, location in enumerate(locations):
            if location[-1] == "Z" and periods[index] == -1:
                periods[index] = steps

        if -1 not in periods:
            return reduce(lcm, periods)


def main() -> None:
    test_input: str = """LR

AAA = (11B, XXX)
11B = (XXX, ZZZ)
ZZZ = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""
    test_input_parsed: list[str] = test_input.split("\n")
    test_output_part_1_expected: OUTPUT_TYPE = 2
    test_output_part_2_expected: OUTPUT_TYPE = 6

    file_location: str = "Day 8/input.txt"
    input_file: list[str] = open(file_location, "r").readlines()

    test_output_part_1: OUTPUT_TYPE = main_part_1(test_input_parsed)
    test_output_part_2: OUTPUT_TYPE = 6

    if test_output_part_1_expected == test_output_part_1:
        print(f"Part 1: {main_part_1(input_file)}")
    else:
        print(f"Part 1 testing error: ")
        print(f"Test input: {test_input}")
        print(f"Expected output: {test_output_part_1_expected}")
        print(f"Got: {test_output_part_1}")
        print()

    if test_output_part_2_expected == test_output_part_2:
        print(f"Part 2: {main_part_2(input_file)}")
    else:
        print(f"Part 2 testing error: ")
        print(f"Test input: {test_input}")
        print(f"Expected output: {test_output_part_2_expected}")
        print(f"Got: {test_output_part_2}")


if __name__ == "__main__":
    main()
