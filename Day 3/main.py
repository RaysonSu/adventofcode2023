OUTPUT_TYPE = int


def main_part_1(inp: list[str]) -> OUTPUT_TYPE:
    ret: int = 0
    row: int = 0

    for index in range(len(inp)):
        inp[index] = "." + inp[index].strip() + "."

    inp.insert(0, "." * len(inp[0]))
    inp.append("." * len(inp[0]))

    while row < len(inp):
        column: int = 0
        eaten: str = ""
        while column < len(inp[row]):
            if inp[row][column].isnumeric():
                eaten += inp[row][column]
            elif eaten:
                neighbours: str = ""
                for row_diffrence in [-1, 0, 1]:
                    neighbours += inp[row + row_diffrence][max(
                        0, column - len(eaten) - 1):column + 1]

                if True in [char in neighbours for char in "@#$%&*-=+/"]:
                    ret += int(eaten)
                eaten = ""
            column += 1
        row += 1

    return ret


def main_part_2(inp: list[str]) -> OUTPUT_TYPE:
    ret: int = 0
    seen: dict[tuple[int, int], int] = {}
    row: int = 0

    for index in range(len(inp)):
        inp[index] = "." + inp[index].strip() + "."

    inp.insert(0, "." * len(inp[0]))
    inp.append("." * len(inp[0]))

    while row < len(inp):
        column: int = 0
        eaten: str = ""
        while column < len(inp[row]):
            if inp[row][column].isnumeric():
                eaten += inp[row][column]
            elif eaten:
                for row_diffrence in [-1, 0, 1]:
                    for column_diffrence in range(-len(eaten) - 1, 1):
                        if inp[row + row_diffrence][column + column_diffrence] != "*":
                            continue

                        coord: tuple[int, int] = (
                            row + row_diffrence, column + column_diffrence)

                        if coord in seen.keys():
                            ret += seen[coord] * int(eaten)
                        else:
                            seen[coord] = int(eaten)
                eaten = ""
            column += 1
        row += 1

    return ret


def main() -> None:
    test_input: str = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""
    test_input_parsed: list[str] = test_input.split("\n")
    test_output_part_1_expected: OUTPUT_TYPE = 4361
    test_output_part_2_expected: OUTPUT_TYPE = 467835

    file_location: str = "Day 3/input.txt"
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
