OUTPUT_TYPE = int


def main_part_1(inp: list[str]) -> OUTPUT_TYPE:
    seen: dict[tuple[str, tuple[int, ...]], int] = {}

    def do_line(data: str, values: tuple[int, ...]) -> int:
        if values == ():
            return int("#" not in data)

        if (data, values) in seen.keys():
            return seen[(data, values)]

        ret: int = 0
        fit: int = values[0]
        goal: str = "#" * fit + "."
        for i in range(min((data.index("#") + 1)if "#" in data else len(data), len(data))):
            window: str = data[i:i+fit+1]
            for goal_char, char in zip(goal, window):
                if char != goal_char and char in "#.":
                    break
            else:
                ret += do_line(data[i+fit+1:], values[1:])

        seen[(data, values)] = ret
        return ret

    ret: int = 0
    for line in inp:
        ret += do_line(line.split(" ")[0] + ".",
                       tuple(eval(f"[{line.split(' ')[1].strip()}]")))

    return ret


def main_part_2(inp: list[str]) -> OUTPUT_TYPE:
    seen: dict[tuple[str, tuple[int, ...]], int] = {}

    def do_line(data: str, values: tuple[int, ...]) -> int:
        if values == ():
            return int("#" not in data)

        if (data, values) in seen.keys():
            return seen[(data, values)]

        ret: int = 0
        fit: int = values[0]
        goal: str = "#" * fit + "."
        for i in range(min((data.index("#") + 1)if "#" in data else len(data), len(data))):
            window: str = data[i:i+fit+1]
            for goal_char, char in zip(goal, window):
                if char != goal_char and char in "#.":
                    break
            else:
                ret += do_line(data[i+fit+1:], values[1:])

        seen[(data, values)] = ret
        return ret

    ret: int = 0
    for line in inp:
        ret += do_line(((line.split(" ")[0]+"?") * 5)[:-1] + ".",
                       tuple(eval(f"[{((line.split(' ')[1].strip() + ',') * 5)[:-1]}]")))

    return ret


def main() -> None:
    test_input: str = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""
    test_input_parsed: list[str] = test_input.split("\n")
    test_output_part_1_expected: OUTPUT_TYPE = 21
    test_output_part_2_expected: OUTPUT_TYPE = 525152

    file_location: str = "Day 12/input.txt"
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
