from itertools import combinations
OUTPUT_TYPE = int


def transpose(grid: list[list[str]]) -> list[list[str]]:
    return [[grid[j][i] for j in range(len(grid))] for i in range(len(grid[0]))]

def replace(grid: list[list[str]]) -> list[list[str]]:
    return [["%" for _ in range(len(row))] if len(set(row)) == 1 else row  for row in grid]

def compute_indexes(grid: list[list[str]], factor: int) -> list[int]:
    ret: list[int] = []

    for row in grid:
        real_x_coord: int = 0
        for char in row:
            if char == "%":
                real_x_coord += factor - 1
            if char == "#":
                ret.append(real_x_coord)
            real_x_coord += 1
    
    return ret

def expansion(inp: list[str], factor: int) -> OUTPUT_TYPE:
    grid: list[list[str]] = [[char for char in row if char != "\n"] for row in inp]
    grid_transpose: list[list[str]] = transpose(grid)

    x_replaced: list[list[str]] = replace(grid_transpose)
    y_replaced: list[list[str]] = replace(grid)
    
    x_coords: list[int] = compute_indexes(transpose(y_replaced), factor)
    y_coords: list[int] = compute_indexes(transpose(x_replaced), factor)
    
    x_coords.sort()
    y_coords.sort()

    ret: int = 0
    for pair in combinations(x_coords, 2):
        ret += max(pair) - min(pair)

    for pair in combinations(y_coords, 2):
        ret += max(pair) - min(pair)
    
    return ret

def main_part_1(inp: list[str]) -> OUTPUT_TYPE:
    return expansion(inp, 2)

def main_part_2(inp: list[str]) -> OUTPUT_TYPE:
    return expansion(inp, 10 ** 6)


def main() -> None:
    test_input: str = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""
    test_input_parsed: list[str] = test_input.split("\n")
    test_output_part_1_expected: OUTPUT_TYPE = 374
    test_output_part_2_expected: OUTPUT_TYPE = 82000210

    file_location: str = "python/Advent of Code/2023/Day 11/input.txt"
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
