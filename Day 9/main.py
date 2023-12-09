OUTPUT_TYPE = int


def parse_inp(inp: list[str]) -> list[list[int]]:
    ret: list[list[int]] = []
    for row in inp:
        ret.append(list(map(int, row.strip().split(" "))))
    return ret


def extrapolate(history: list[int], forward: False = True) -> int:
    histories: list[list[int]] = [history]
    while sum(map(lambda x: x*x, history)):
        history = [history[i + 1] - history[i]
                   for i in range(len(history) - 1)]
        histories.append(history)

    total: int = 0
    if forward:
        for history in histories:
            total += history[-1]
    else:
        for history in histories[::-1]:
            total = history[0] - total

    return total


def main_part_1(inp: list[str]) -> OUTPUT_TYPE:
    histories: list[list[int]] = parse_inp(inp)
    ret: int = 0
    for history in histories:
        ret += extrapolate(history)
    return ret


def main_part_2(inp: list[str]) -> OUTPUT_TYPE:
    histories: list[list[int]] = parse_inp(inp)
    ret: int = 0
    for history in histories:
        ret += extrapolate(history, False)
    return ret


def main() -> None:
    test_input: str = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""
    test_input_parsed: list[str] = test_input.split("\n")
    test_output_part_1_expected: OUTPUT_TYPE = 114
    test_output_part_2_expected: OUTPUT_TYPE = 2

    file_location: str = "Day 9/input.txt"
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
