import numpy as np
OUTPUT_TYPE = int


# thanks stack overflow: https://stackoverflow.com/questions/24467972/calculate-area-of-polygon-given-x-y-coordinates
def poly_area(x: list[int], y: list[int]) -> int:
    return np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1))) // 2


def main_part_1(inp: list[str]) -> OUTPUT_TYPE:
    locations_x: list[int] = [0]
    locations_y: list[int] = [0]
    points: int = 0
    for line in inp:
        instructions: list[str] = line.strip().split(" ")
        current_x: int = locations_x[-1]
        current_y: int = locations_y[-1]
        amount: int = int(instructions[1])
        direction: str = instructions[0]
        if direction == "U":
            locations_x.append(current_x - amount)
            locations_y.append(current_y)
        if direction == "D":
            locations_x.append(current_x + amount)
            locations_y.append(current_y)
        if direction == "L":
            locations_x.append(current_x)
            locations_y.append(current_y - amount)
        if direction == "R":
            locations_x.append(current_x)
            locations_y.append(current_y + amount)
        points += amount
    return poly_area(locations_x, locations_y) + points // 2 + 1


def main_part_2(inp: list[str]) -> OUTPUT_TYPE:
    locations_x: list[int] = [0]
    locations_y: list[int] = [0]
    points: int = 0
    for line in inp:
        instructions: list[str] = line.strip().split(" ")
        current_x: int = locations_x[-1]
        current_y: int = locations_y[-1]
        amount: int = int(instructions[2][2:-2], 16)
        direction: str = ["R", "D", "L", "U"][int(instructions[2][-2])]
        if direction == "U":
            locations_x.append(current_x - amount)
            locations_y.append(current_y)
        if direction == "D":
            locations_x.append(current_x + amount)
            locations_y.append(current_y)
        if direction == "L":
            locations_x.append(current_x)
            locations_y.append(current_y - amount)
        if direction == "R":
            locations_x.append(current_x)
            locations_y.append(current_y + amount)
        points += amount
    return poly_area(locations_x, locations_y) + points // 2 + 1


def main() -> None:
    test_input: str = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""
    test_input_parsed: list[str] = test_input.split("\n")
    test_output_part_1_expected: OUTPUT_TYPE = 62
    test_output_part_2_expected: OUTPUT_TYPE = 952408144115

    file_location: str = "Day 18/input.txt"
    input_file: list[str] = open(file_location, "r").readlines()

    test_output_part_1: OUTPUT_TYPE = main_part_1(test_input_parsed)
    test_output_part_2: OUTPUT_TYPE = main_part_2(test_input_parsed)

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
