from itertools import combinations
from scipy.optimize import fsolve
from numpy.linalg import norm
from random import randint
from typing import Callable
OUTPUT_TYPE = int


def random_coords() -> tuple[float, float, float, float, float, float]:
    return (
        float(randint(200000000000000, 400000000000000)),
        float(randint(200000000000000, 400000000000000)),
        float(randint(200000000000000, 400000000000000)),
        0.0,
        0.0,
        0.0
    )


def parse_inp(inp: list[str]) -> list[tuple[tuple[int, int, int], tuple[int, int, int]]]:
    ret: list[tuple[tuple[int, int, int], tuple[int, int, int]]] = []
    for line in inp:
        ret.append((
            eval(
                f"({''.join([x for x in line.split('@')[0] if x in '1234567890-,'])})"),
            eval(
                f"({''.join([x for x in line.split('@')[1] if x in '1234567890-,'])})")
        ))

    return ret


def conv(vec: tuple[tuple[int, int, int], tuple[int, int, int]]) -> tuple[int, int, int]:
    return (vec[1][1], -vec[1][0], vec[0][0] * vec[1][1] - vec[0][1] * vec[1][0])


def make_equations(hailstone_1: tuple[tuple[int, int, int], tuple[int, int, int]],
                   hailstone_2: tuple[tuple[int, int, int], tuple[int, int, int]],
                   hailstone_3: tuple[tuple[int, int, int], tuple[int, int, int]]
                   ) -> Callable[[tuple[float, float, float, float, float, float]], tuple[float, float, float, float, float, float]]:

    X_0: tuple[int, int, int]
    V_0: tuple[int, int, int]
    X_1: tuple[int, int, int]
    V_1: tuple[int, int, int]
    X_2: tuple[int, int, int]
    V_2: tuple[int, int, int]

    X_0, V_0 = hailstone_1
    X_1, V_1 = hailstone_2
    X_2, V_2 = hailstone_3

    x00: int
    x01: int
    x02: int
    v00: int
    v01: int
    v02: int
    x10: int
    x11: int
    x12: int
    v10: int
    v11: int
    v12: int
    x20: int
    x21: int
    x22: int
    v20: int
    v21: int
    v22: int

    x00, x01, x02 = X_0
    v00, v01, v02 = V_0
    x10, x11, x12 = X_1
    v10, v11, v12 = V_1
    x20, x21, x22 = X_2
    v20, v21, v22 = V_2

    def equation(p: tuple[float, float, float, float, float, float]) -> tuple[float, float, float, float, float, float]:
        x: float
        y: float
        z: float
        vx: float
        vy: float
        vz: float

        x, y, z, vx, vy, vz = p

        t0: float
        t1: float
        t2: float

        t0 = -(x - x00) / (vx - v00)
        t1 = -(x - x10) / (vx - v10)
        t2 = -(x - x20) / (vx - v20)

        return (
            y - x01 + (vy - v01) * t0,
            z - x02 + (vz - v02) * t0,

            y - x11 + (vy - v11) * t1,
            z - x12 + (vz - v12) * t1,

            y - x21 + (vy - v21) * t2,
            z - x22 + (vz - v22) * t2,
        )

    return equation


def main_part_1(inp: list[str]) -> OUTPUT_TYPE:
    hailstones: list[tuple[tuple[int, int, int], tuple[int, int, int]]]
    hailstones = parse_inp(inp)

    pairs: combinations[tuple[tuple[tuple[int, int, int], tuple[int, int, int]],
                              tuple[tuple[int, int, int], tuple[int, int, int]]]]
    pairs = combinations(hailstones, 2)
    ret: int = 0
    for x, y in pairs:
        a: int
        b: int
        c: int
        d: int
        e: int
        f: int

        a, b, e = conv(x)
        c, d, f = conv(y)

        det: int = a * d - b * c

        if det == 0:
            continue

        xcoli: float = (d * e - b * f) / det
        ycoli: float = (-c * e + a * f) / det

        if xcoli < 200000000000000 or xcoli > 400000000000000:
            continue

        if ycoli < 200000000000000 or ycoli > 400000000000000:
            continue

        t_x: float = (xcoli - x[0][0]) / x[1][0]
        t_y: float = (xcoli - y[0][0]) / y[1][0]

        if t_x < 0 or t_y < 0:
            continue

        ret += 1

    return ret


def main_part_2(inp: list[str]) -> OUTPUT_TYPE:
    hailstones: list[tuple[tuple[int, int, int], tuple[int, int, int]]]
    hailstones = parse_inp(inp)

    equations: Callable[[tuple[float, float, float, float, float, float]],
                        tuple[float, float, float, float, float, float]]
    equations = make_equations(hailstones[0], hailstones[1], hailstones[2])

    while True:
        guess: tuple[float, float, float, float, float,
                     float] = fsolve(equations, random_coords())
        diff: float = float(norm(equations(guess)))

        if diff < 1:
            return round(guess[0] + guess[1] + guess[2])


def main() -> None:
    test_input: str = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""
    test_input_parsed: list[str] = test_input.split("\n")
    test_output_part_1_expected: OUTPUT_TYPE = 0
    test_output_part_2_expected: OUTPUT_TYPE = 47

    file_location: str = "Day 24/input.txt"
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
