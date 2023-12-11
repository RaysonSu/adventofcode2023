import numpy as np
OUTPUT_TYPE = int

# thanks stack overflow: https://stackoverflow.com/questions/24467972/calculate-area-of-polygon-given-x-y-coordinates


def poly_area(x: list[int], y: list[int]) -> int:
    return np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1))) // 2


def main_part_1(inp: list[str]) -> OUTPUT_TYPE:
    # ensures there's a \n at the end of each line
    inp = [line.replace("\n", "") + "\n" for line in inp]

    x_length: int = len(inp[0])
    grid: str = "".join(inp)

    initial: int = grid.index("S")
    tile_directions: dict[str, list[tuple[int, int]]] = {
        "|": [(0, 0), (x_length, 1), (0, 0), (-x_length, 3)],
        "-": [(-1, 0), (0, 0), (1, 2), (0, 0)],
        "J": [(0, 0), (-1, 0), (-x_length, 3), 0],
        "F": [(x_length, 1), (0, 0), (0, 0), (1, 2)],
        "L": [(-x_length, 3), (1, 2), (0, 0), (0, 0)],
        "7": [(0, 0), (0, 0), (x_length, 1), (-1, 0)],
    }
    path_locations: list[int] = [initial - 1, initial + x_length,
                                 initial + 1, initial - x_length]
    path_directions: list[int] = [0, 1, 2, 3]
    time: int = 1

    while len(set(path_locations)) == len(path_locations):
        time += 1
        for i in range(4):
            if path_locations[i] < 0:
                continue

            if grid[path_locations[i]] not in "|-LJ7F":
                path_locations[i] = -i - 1
                continue

            change: tuple[int, int] = tile_directions[grid[path_locations[i]]
                                                      ][path_directions[i]]
            if change == (0, 0):
                path_locations[i] = -i - 1
                continue

            path_locations[i] += change[0]
            path_directions[i] = change[1]
    return time


def main_part_2(inp: list[str]) -> OUTPUT_TYPE:
    # ensures there's a \n at the end of each line
    inp = [line.replace("\n", "") + "\n" for line in inp]

    x_length: int = len(inp[0])
    grid: str = "".join(inp)

    initial: int = grid.index("S")
    tile_directions: dict[str, list[tuple[int, int]]] = {
        "|": [(0, 0), (x_length, 1), (0, 0), (-x_length, 3)],
        "-": [(-1, 0), (0, 0), (1, 2), (0, 0)],
        "J": [(0, 0), (-1, 0), (-x_length, 3), 0],
        "F": [(x_length, 1), (0, 0), (0, 0), (1, 2)],
        "L": [(-x_length, 3), (1, 2), (0, 0), (0, 0)],
        "7": [(0, 0), (0, 0), (x_length, 1), (-1, 0)],
    }
    path_locations: list[int] = [initial - 1, initial + x_length,
                                 initial + 1, initial - x_length]
    path_directions: list[int] = [0, 1, 2, 3]
    points_visited: list[list[int]] = [[initial, location]
                                       for location in path_locations]
    valid_points: list[int] = [0, 1, 2, 3]
    while len(set(path_locations)) == len(path_locations):
        for i in range(4):
            if path_locations[i] < 0:
                continue

            if grid[path_locations[i]] not in "|-LJ7F":
                path_locations[i] = -i - 1
                valid_points.remove(i)
                continue

            change: tuple[int, int] = tile_directions[grid[path_locations[i]]
                                                      ][path_directions[i]]
            if change == (0, 0):
                path_locations[i] = -i - 1
                valid_points.remove(i)
                continue

            path_locations[i] += change[0]
            path_directions[i] = change[1]
            points_visited[i].append(path_locations[i])

    polygon_points: list[int] = []
    polygon_points.extend(points_visited[valid_points[0]])
    polygon_points.extend(points_visited[valid_points[1]][::-1][1:-1])

    x_coords: list[int] = [point % x_length for point in polygon_points]
    y_coords: list[int] = [point // x_length for point in polygon_points]

    return poly_area(x_coords, y_coords) - len(polygon_points) // 2 + 1


def main() -> None:
    test_input: str = """..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
.........."""
    test_input_parsed: list[str] = test_input.split("\n")
    test_output_part_1_expected: OUTPUT_TYPE = 22
    test_output_part_2_expected: OUTPUT_TYPE = 4

    file_location: str = "python/Advent of Code/2023/Day 10/input.txt"
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
