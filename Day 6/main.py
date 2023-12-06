OUTPUT_TYPE = int


def parse_inp(inp: list[str]) -> None:
    return


def solve_quadratic(b: int | float, c: int | float) -> float:
    return (-b - (b ** 2 - 4 * c) ** 0.5) / 2


def main_part_1(inp: list[str]) -> OUTPUT_TYPE:
    times: list[str] = [time
                        for time
                        in inp[0].strip("\n").split(" ")
                        if time and time.isnumeric()]

    distances: list[str] = [distance
                            for distance
                            in inp[1].split(" ")
                            if distance and distance.isnumeric()]

    margins: int = 1
    for time, distance, in zip(times, distances):
        minimum_time = solve_quadratic(-int(time), int(distance))
        margins *= int(time) - 2 * int(minimum_time) - 1
    return margins


def main_part_2(inp: list[str]) -> OUTPUT_TYPE:
    time: int = int(inp[0].replace(" ", "").split(":")[1])
    distance: int = int(inp[1].replace(" ", "").split(":")[1])

    minimum_time: float = solve_quadratic(-int(time), int(distance))
    return int(time) - 2 * int(minimum_time) - 1


def main() -> None:
    test_input: str = """Time:      7  15   30
Distance:  9  40  200"""
    test_input_parsed: list[str] = test_input.split("\n")
    test_output_part_1_expected: OUTPUT_TYPE = 288
    test_output_part_2_expected: OUTPUT_TYPE = 71503

    file_location: str = "Day 6/input.txt"
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
