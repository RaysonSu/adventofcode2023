OUTPUT_TYPE = int


def str_assign(string: str, index: int, item: str) -> str:
    return string[:index] + item + string[index+1:]


def fit_quadratic(x1: int, y1: int, x2: int, y2: int, x3: int, y3: int) -> tuple[int, int, int]:
    a1: int = x2 ** 2 - x1 ** 2
    b1: int = x2 - x1
    d1: int = y2 - y1
    a2: int = x3 ** 2 - x2 ** 2
    b2: int = x3 - x2
    d2: int = y3 - y2
    b_mul: int = -b2 // b1
    a3: int = b_mul * a1 + a2
    d3: int = b_mul * d1 + d2

    a: int = d3 // a3
    b: int = (d1 - a1 * a) // b1
    c: int = y1 - a * x1 ** 2 - b * x1

    return a, b, c


def main_part_1(inp: list[str]) -> OUTPUT_TYPE:
    start: tuple[int, int]
    for row_index, row in enumerate(inp):
        for col_index, char in enumerate(row):
            if char == "S":
                start = (col_index, row_index)
        row = row.strip()

    points: set[tuple[int, int]] = {start}
    for _ in range(64):
        new_points: set[tuple[int, int]] = set()
        for x, y in points:
            for x_diff, y_diff in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                new_x: int = x + x_diff
                new_y: int = y + y_diff
                try:
                    if inp[new_y][new_x] in ".S" and new_y >= 0 and new_x >= 0:
                        new_points.add((new_x, new_y))
                except:
                    pass
        points = new_points

    return len(points)


def main_part_2(inp: list[str]) -> OUTPUT_TYPE:
    start: tuple[int, int]
    for row_index, row in enumerate(inp):
        for col_index, char in enumerate(row):
            if char == "S":
                start = (col_index, row_index)
        inp[row_index] = inp[row_index].strip()

    points: set[tuple[int, int]] = {start}
    hashed: set[int] = set()
    initial: int = -1
    count: int = 1
    xs: list[int] = []
    ys: list[int] = []

    while True:
        new_points: set[tuple[int, int]] = set()
        for x, y in points:
            for x_diff, y_diff in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                new_x: int = x + x_diff
                new_y: int = y + y_diff
                if inp[new_y % len(inp)][new_x % len(inp[0])] != "#":
                    new_points.add((new_x, new_y))
        points = new_points

        counts: list[list[int]] = [
            [0 for _ in range(len(inp[0]))] for _ in range(len(inp))]
        for x, y in new_points:
            counts[y % len(inp)][x % len(inp[0])] += 1

        if initial == -1:
            i_copy = inp.copy()
            for row_index, row in enumerate(inp):
                for col_index, char in enumerate(row):
                    if char != "#":
                        i_copy[row_index] = str_assign(i_copy[row_index], col_index, hex(
                            counts[row_index][col_index] % 2)[2:])

            new: int = hash("".join(i_copy))
            if new in hashed:
                initial = count
            else:
                hashed.add(new)
        elif (26501365 - count) % len(inp[0]) == 0:
            xs.append(count)
            ys.append(sum(map(sum, counts)))

        if len(xs) == 3:
            break

        count += 1

    a: int
    b: int
    c: int

    xs = [(x - initial) // len(inp[0]) for x in xs]
    a, b, c = fit_quadratic(xs[0], ys[0], xs[1], ys[1], xs[2], ys[2])

    x = (26501365 - initial) // len(inp[0])

    return a * x ** 2 + b * x + c


def main() -> None:
    test_input: str = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""
    test_input_parsed: list[str] = test_input.split("\n")
    test_output_part_1_expected: OUTPUT_TYPE = 42
    test_output_part_2_expected: OUTPUT_TYPE = 470149643712804

    file_location: str = "Day 21/input.txt"
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
