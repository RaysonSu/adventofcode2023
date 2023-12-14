from collections import defaultdict
OUTPUT_TYPE = int


def transpose(grid: tuple[str, ...]) -> tuple[str, ...]:
    return tuple([
        "".join(grid[j][i] for j in range(len(grid)) if grid[j][i] != "\n")
        for i in range(len(grid[-1]))
    ])


def rotate90(grid: tuple[str, ...]) -> tuple[str, ...]:
    return transpose(grid)[::-1]


def transform_row(row: str) -> str:
    new_str: str = ""
    for index, char in enumerate(row):
        if char == "#":
            while len(new_str) < index:
                new_str += "."
            new_str += "#"
        elif char == "O":
            new_str += "O"

    new_str = new_str[::-1]
    while len(new_str) < len(row):
        new_str = "." + new_str

    return new_str[::-1]


def transform_grid(grid: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(map(transform_row, grid))


def value_row(row: str) -> int:
    ret: int = 0
    for i, char in enumerate(row[::-1], 1):
        if char == "O":
            ret += i
    return ret


def compute_row(row) -> int:
    return value_row(transform_row(row))


def calc_north(inp: tuple[str, ...]) -> int:
    return sum(map(value_row, inp))


def main_part_1(inp: list[str]) -> OUTPUT_TYPE:
    grid: tuple[str, ...] = tuple(inp)
    return sum(map(compute_row, transpose(grid)))


def main_part_2(inp: list[str]) -> OUTPUT_TYPE:
    grid: tuple[str, ...] = tuple(inp)
    seen: defaultdict[tuple[str, ...], int] = defaultdict(lambda: 0)
    periodic_values: list[int] = []
    initial: int = -1
    cycles: int = 0

    grid = transpose(grid)
    seen[grid] += 1

    while True:
        for _ in range(4):
            grid = rotate90(transform_grid(grid))

        seen[grid] += 1

        if max(seen.values()) >= 3:
            return periodic_values[(10 ** 9 - initial - 1) % (initial - cycles)]
        elif max(seen.values()) >= 2:
            periodic_values.append(calc_north(grid))
            if initial == -1:
                initial = cycles

        cycles += 1


def main() -> None:
    test_input: str = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""
    test_input_parsed: list[str] = test_input.split("\n")
    test_output_part_1_expected: OUTPUT_TYPE = 136
    test_output_part_2_expected: OUTPUT_TYPE = 64

    file_location: str = "Day 14/input.txt"
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
