OUTPUT_TYPE = int


def transpose(grid: list[str]) -> list[str]:
    return ["".join([grid[j][i] for j in range(len(grid))]) for i in range(len(grid[0]))]


def parse_inp(inp: list[str]) -> list[tuple[list[str], list[str]]]:
    st: str = "".join(inp)
    ret: list[tuple[list[str], list[str]]] = []
    for i in st.split("\n\n"):
        ret.append((i.split("\n"), transpose(i.split("\n"))))
    return ret


def parse_grid(inp: list[str]):
    grid: set[tuple[int, int]] = set()
    for y, row in enumerate(inp):
        for x, char in enumerate(row.strip()):
            if char == "#":
                grid.add((x, y))
    return grid


def main_part_2(inp: list[str]) -> OUTPUT_TYPE:
    p: list[tuple[list[str], list[str]]] = parse_inp(inp)
    ret: int = 0
    for rows, columns in p:
        failed: bool = True
        for i in range(1, len(columns)):
            left: list[str] = columns[i-1::-1]
            right: list[str] = columns[i:]

            length: int = min(len(left), len(right))
            left = left[:length]
            right = right[:length]

            left_set: set[tuple[int, int]] = parse_grid(left)
            right_set: set[tuple[int, int]] = parse_grid(right)

            diffrence: set[tuple[int, int]] = left_set.difference(
                right_set).union(right_set.difference(left_set))
            if len(diffrence) == 1:
                ret += i
                failed = False

        if not failed:
            continue

        for i in range(1, len(rows)):
            left = rows[i-1::-1]
            right = rows[i:]

            length = min(len(left), len(right))
            left = left[:length]
            right = right[:length]

            left_set = parse_grid(left)
            right_set = parse_grid(right)

            diffrence = left_set.difference(right_set).union(
                right_set.difference(left_set))
            if len(diffrence) == 1:
                ret += i * 100
                break
        else:
            print("Crap!")

    return ret


def main_part_1(inp: list[str]) -> OUTPUT_TYPE:
    p: list[tuple[list[str], list[str]]] = parse_inp(inp)
    ret: int = 0

    for rows, columns in p:
        for i in range(1, len(columns)):
            left: list[str] = columns[i-1::-1]
            right: list[str] = columns[i:]

            length: int = min(len(left), len(right))
            left = left[:length]
            right = right[:length]
            if left == right:
                ret += i
                break
        else:
            for i in range(1, len(rows)):
                left = rows[i-1::-1]
                right = rows[i:]

                length = min(len(left), len(right))
                left = left[:length]
                right = right[:length]
                if left == right:
                    ret += i * 100
                    break
    return ret


def main() -> None:
    test_input: str = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""
    test_input_parsed: list[str] = test_input.splitlines(True)
    test_output_part_1_expected: OUTPUT_TYPE = 405
    test_output_part_2_expected: OUTPUT_TYPE = 400

    file_location: str = "Day 13/input.txt"
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
