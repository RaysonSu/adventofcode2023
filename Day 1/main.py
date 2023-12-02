OUTPUT_TYPE = int


def get_digit(string: str, replacer: list[str], reverse: bool) -> str:
    for index in range(len(string)):
        target_index: int = (-index - 1) if reverse else index
        if string[target_index].isnumeric():
            return string[target_index]

        for digit, name in enumerate(replacer):
            if (not reverse and string[index:].startswith(name)) \
                    or (reverse and string[:len(string) - index].endswith(name)):
                return str(digit)

    return ""


def main_part_1(inp: list[str]) -> int:
    ret: int = 0
    for line in inp:
        first: str = get_digit(line, [], False)
        last: str = get_digit(line, [], True)
        ret += int(first + last)
    return ret


def main_part_2(inp: list[str]) -> int:
    replacer: list[str] = ["zero", "one", "two", "three",
                           "four", "five", "six", "seven", "eight", "nine"]
    ret: int = 0

    for line in inp:
        line = line.strip()
        first: str = get_digit(line, replacer, False)
        last: str = get_digit(line, replacer, True)
        ret += int(first + last)
    return ret


def main() -> None:
    test_input: str = """two1nine
eightwo1three
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""
    test_input_parsed: list[str] = test_input.split("\n")
    test_output_part_1_expected: OUTPUT_TYPE = 220
    test_output_part_2_expected: OUTPUT_TYPE = 281

    file_location: str = "python/Advent of Code/2023/Day 1/input.txt"
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
