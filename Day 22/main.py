from __future__ import annotations
OUTPUT_TYPE = int


class Range:
    def __init__(self, low: int, high: int) -> None:
        self.low: int = low
        self.high: int = high

    def __contains__(self, point: int) -> bool:
        return self.low <= point and point <= self.high

    def __iter__(self) -> range:
        return range(self.low, self.high + 1)

    def is_valid(self) -> bool:
        return self.high >= self.low

    def length(self) -> int:
        return self.high - self.low + 1

    def intersect(self, other: Range) -> Range:
        return Range(max(self.low, other.low), min(self.high, other.high))

    def remove(self, other: Range) -> list[Range]:
        new_ranges: list[Range] = []
        if self.high <= other.high and self.low >= other.low:
            pass

        elif self.high > other.high and self.low < other.low:
            new_ranges.append(Range(self.low, other.low - 1))
            new_ranges.append(Range(other.high + 1, self.high))

        elif self.high <= other.high and self.high >= other.low:
            new_ranges.append(Range(self.low, other.low - 1))

        elif self.low >= other.low and self.low <= other.high:
            new_ranges.append(Range(other.high + 1, self.high))

        else:
            new_ranges.append(self)
        return new_ranges

    def union(self, other: Range) -> list[Range]:
        new_ranges: list[Range] = []
        if self.high <= other.high and self.low >= other.low:
            new_ranges.append(self)

        elif self.high > other.high and self.low < other.low:
            new_ranges.append(other)

        elif self.high <= other.high and self.high >= other.low:
            new_ranges.append(Range(self.low, other.high))

        elif self.low >= other.low and self.low <= other.high:
            new_ranges.append(Range(other.low, self.high))

        else:
            new_ranges.append(self)
            new_ranges.append(other)
        return new_ranges

    def shift(self, amount: int) -> None:
        self.low += amount
        self.high += amount


class Cuboid:
    def __init__(self, x: Range, y: Range, z: Range) -> None:
        self.x_bounds: Range = x
        self.y_bounds: Range = y
        self.z_bounds: Range = z

    def __contains__(self, point: tuple[int, int, int]) -> bool:
        return point[0] in self.x_bounds and point[1] in self.y_bounds and point[2] in self.z_bounds

    def is_valid(self) -> bool:
        return self.x_bounds.is_valid() and self.y_bounds.is_valid() and self.z_bounds.is_valid()

    def volume(self) -> int:
        return self.x_bounds.length() * self.y_bounds.length() * self.z_bounds.length()

    def intersect(self, other: Cuboid) -> Cuboid:
        return Cuboid(
            self.x_bounds.intersect(other.x_bounds),
            self.y_bounds.intersect(other.y_bounds),
            self.z_bounds.intersect(other.z_bounds)
        )

    def intersects(self, other: Cuboid) -> bool:
        return self.intersect(other).is_valid()

    def remove(self, other: Cuboid) -> list[Cuboid]:
        new_cuboids: list[Cuboid] = []
        # main x-axis
        for x_axis in self.x_bounds.remove(other.x_bounds):
            new_cuboids.append(Cuboid(
                x_axis,
                self.y_bounds,
                self.z_bounds
            ))

        # main y-axis
        for y_axis in self.y_bounds.remove(other.y_bounds):
            new_cuboids.append(Cuboid(
                self.x_bounds.intersect(other.x_bounds),
                y_axis,
                self.z_bounds
            ))

        # main z-axis
        for z_axis in self.z_bounds.remove(other.z_bounds):
            new_cuboids.append(Cuboid(
                self.x_bounds.intersect(other.x_bounds),
                self.y_bounds.intersect(other.y_bounds),
                z_axis
            ))

        return [cuboid for cuboid in new_cuboids if cuboid.is_valid()]

    def union(self, other: Cuboid) -> list[Cuboid]:
        new_cuboids: list[Cuboid] = []
        new_cuboids.append(self)
        new_cuboids.extend(other.remove(self))
        return new_cuboids

    def under(self) -> Cuboid:
        return Cuboid(
            self.x_bounds,
            self.y_bounds,
            Range(self.z_bounds.low, self.z_bounds.low)
        )

    def project(self, plane: str) -> Cuboid:
        new_x_bounds: Range = self.x_bounds
        new_y_bounds: Range = self.y_bounds
        new_z_bounds: Range = self.z_bounds

        if "x" not in plane:
            new_x_bounds = Range(0, 0)

        if "y" not in plane:
            new_y_bounds = Range(0, 0)

        if "z" not in plane:
            new_z_bounds = Range(0, 0)

        return Cuboid(
            new_x_bounds,
            new_y_bounds,
            new_z_bounds
        )


class Cuboids:  # stole this code from last year!
    def __init__(self) -> None:
        self.cuboids: list[Cuboid] = []

    def __contains__(self, point: tuple[int, int, int]) -> bool:
        for cuboid in self.cuboids:
            if point in cuboid:
                return True

        return False

    def collapse(self) -> None:
        self.cuboids.sort(key=lambda x: x.z_bounds.low)
        new_cuboids: list[Cuboid] = []

        for cuboid in self.cuboids:
            while True:
                cuboid.z_bounds.shift(-1)
                succeded: bool = True
                for other_cuboid in new_cuboids:
                    if cuboid.intersects(other_cuboid):
                        succeded = False
                        break

                if not succeded or cuboid.z_bounds.low == 0:
                    cuboid.z_bounds.shift(1)
                    new_cuboids.append(cuboid)
                    break

#            print(
#                f"\r{len(new_cuboids)}/{len(self.cuboids)} cuboids collapsed", end="")

        self.cuboid = new_cuboids

    def volume(self) -> int:
        ret: int = 0
        for cuboid in self.cuboids:
            ret += cuboid.volume()
        return ret

    def add_cuboid(self, cuboid: Cuboid) -> None:
        self.cuboids.append(cuboid)

    def remove_cuboid(self, cuboid: Cuboid) -> None:
        new_cuboids: list[Cuboid] = []
        for self_cuboid in self.cuboids:
            new_cuboids.extend(self_cuboid.remove(cuboid))
        self.cuboids = new_cuboids

    def intersect(self, cuboid: Cuboid) -> None:
        new_cuboids: list[Cuboid] = []
        for self_cuboid in self.cuboids:
            new_cuboid: Cuboid = self_cuboid.intersect(cuboid)
            if new_cuboid.is_valid():
                new_cuboids.append(new_cuboid)
        self.cuboids = new_cuboids


def main_part_1(inp: list[str]) -> OUTPUT_TYPE:
    base_cube: Cuboids = Cuboids()
    for line in inp:
        lower: list[int] = list(map(int, line.split("~")[0].split(",")))
        upper: list[int] = list(map(int, line.split("~")[1].split(",")))
        base_cube.add_cuboid(Cuboid(
            Range(lower[0], upper[0]),
            Range(lower[1], upper[1]),
            Range(lower[2], upper[2])
        ))

    base_cube.collapse()

    support: list[list[int]] = [[] for _ in base_cube.cuboids]
    for i, cuboid in enumerate(base_cube.cuboids):
        for j, other_cuboid in enumerate(base_cube.cuboids):
            if i == j:
                continue

            if cuboid.z_bounds.low - 1 != other_cuboid.z_bounds.high:
                continue

            if cuboid.under().project("xy").intersect(other_cuboid.under().project("xy")).is_valid():
                support[i].append(j)

    valid: set[int] = {i for i in range(len(base_cube.cuboids))}
    for supporting in support:
        if len(supporting) == 1:
            valid.discard(supporting[0])

    return len(valid)


def main_part_2(inp: list[str]) -> OUTPUT_TYPE:
    base_cube: Cuboids = Cuboids()
    for line in inp:
        lower: list[int] = list(map(int, line.split("~")[0].split(",")))
        upper: list[int] = list(map(int, line.split("~")[1].split(",")))
        base_cube.add_cuboid(Cuboid(
            Range(lower[0], upper[0]),
            Range(lower[1], upper[1]),
            Range(lower[2], upper[2])
        ))

    base_cube.collapse()

    support: list[list[int]] = [[] for _ in base_cube.cuboids]
    for i, cuboid in enumerate(base_cube.cuboids):
        for j, other_cuboid in enumerate(base_cube.cuboids):
            if i == j:
                continue

            if cuboid.z_bounds.low - 1 != other_cuboid.z_bounds.high:
                continue

            if cuboid.under().project("xy").intersect(other_cuboid.under().project("xy")).is_valid():
                support[i].append(j)

    valid: set[int] = set()
    for supporting in support:
        if len(supporting) == 1:
            valid.add(supporting[0])

    ret: int = 0
    new_support: list[set[int]] = list(map(set, support))
    for i in valid:
        collapsed: set[int] = {i}
        prev_collapsed: set[int] = set()
        while collapsed != prev_collapsed:
            prev_collapsed = collapsed.copy()
            for block_index, block in enumerate(new_support):
                if len(block) == 0:
                    continue

                if block.issubset(collapsed):
                    collapsed.add(block_index)

        ret += len(collapsed) - 1

    return ret


def main() -> None:
    test_input: str = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""
    test_input_parsed: list[str] = test_input.split("\n")
    test_output_part_1_expected: OUTPUT_TYPE = 5
    test_output_part_2_expected: OUTPUT_TYPE = 7

    file_location: str = "Day 22/input.txt"
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
