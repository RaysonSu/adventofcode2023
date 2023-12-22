from __future__ import annotations

OUTPUT_TYPE = int


class Range:
    def __init__(self, low: int, high: int) -> None:
        self.low: int = low
        self.high: int = high

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


class Hypercuboid:
    def __init__(self, x: Range, y: Range, z: Range, w: Range) -> None:
        self.x_bounds: Range = x
        self.y_bounds: Range = y
        self.z_bounds: Range = z
        self.w_bounds: Range = w

    def is_valid(self) -> bool:
        return self.x_bounds.is_valid() and self.y_bounds.is_valid() and self.z_bounds.is_valid() and self.w_bounds.is_valid()

    def volume(self) -> int:
        return self.x_bounds.length() * self.y_bounds.length() * self.z_bounds.length() * self.w_bounds.length()

    def intersect(self, other: Hypercuboid) -> Hypercuboid:
        return Hypercuboid(
            self.x_bounds.intersect(other.x_bounds),
            self.y_bounds.intersect(other.y_bounds),
            self.z_bounds.intersect(other.z_bounds),
            self.w_bounds.intersect(other.w_bounds)
        )

    def remove(self, other: Hypercuboid) -> list[Hypercuboid]:
        new_hypercuboids: list[Hypercuboid] = []
        # main x-axis
        for x_axis in self.x_bounds.remove(other.x_bounds):
            new_hypercuboids.append(Hypercuboid(
                x_axis,
                self.y_bounds,
                self.z_bounds,
                self.w_bounds
            ))

        # main y-axis
        for y_axis in self.y_bounds.remove(other.y_bounds):
            new_hypercuboids.append(Hypercuboid(
                self.x_bounds.intersect(other.x_bounds),
                y_axis,
                self.z_bounds,
                self.w_bounds
            ))

        # main z-axis
        for z_axis in self.z_bounds.remove(other.z_bounds):
            new_hypercuboids.append(Hypercuboid(
                self.x_bounds.intersect(other.x_bounds),
                self.y_bounds.intersect(other.y_bounds),
                z_axis,
                self.w_bounds
            ))

        # main w-axis
        for w_axis in self.w_bounds.remove(other.w_bounds):
            new_hypercuboids.append(Hypercuboid(
                self.x_bounds.intersect(other.x_bounds),
                self.y_bounds.intersect(other.y_bounds),
                self.z_bounds.intersect(other.z_bounds),
                w_axis
            ))

        return [hypercuboid for hypercuboid in new_hypercuboids if hypercuboid.is_valid()]

    def union(self, other: Hypercuboid) -> list[Hypercuboid]:
        new_hypercuboids: list[Hypercuboid] = []
        new_hypercuboids.append(self)
        new_hypercuboids.extend(other.remove(self))
        return new_hypercuboids


class Hypercuboids:  # stole this code from 202
    def __init__(self) -> None:
        self.hypercuboids: list[Hypercuboid] = []

    def volume(self) -> int:
        ret: int = 0
        for hypercuboid in self.hypercuboids:
            ret += hypercuboid.volume()
        return ret

    def add_hypercuboids(self, hypercuboids: Hypercuboids) -> None:
        for hypercuboid in hypercuboids.hypercuboids:
            self.add_hypercuboid(hypercuboid)

    def add_hypercuboid(self, hypercuboid: Hypercuboid) -> None:
        hypercuboids_to_add: list[Hypercuboid] = [hypercuboid]
        self.hypercuboids.extend(hypercuboids_to_add)

    def remove_hypercuboid(self, hypercuboid: Hypercuboid) -> None:
        new_hypercuboids: list[Hypercuboid] = []
        for self_hypercuboid in self.hypercuboids:
            new_hypercuboids.extend(self_hypercuboid.remove(hypercuboid))
        self.hypercuboids = new_hypercuboids

    def intersect(self, hypercuboid: Hypercuboid) -> None:
        new_hypercuboids: list[Hypercuboid] = []
        for self_hypercuboid in self.hypercuboids:
            new_hypercuboid: Hypercuboid = self_hypercuboid.intersect(
                hypercuboid)
            if new_hypercuboid.is_valid():
                new_hypercuboids.append(new_hypercuboid)
        self.hypercuboids = new_hypercuboids

    def copy(self) -> Hypercuboids:
        ret: Hypercuboids = Hypercuboids()
        ret.hypercuboids = self.hypercuboids.copy()
        return ret


def parse_inp(inp: list[str]) -> tuple[dict[str, list[tuple[str, bool, int, str]]], list[dict[str, int]]]:
    inp = list(map(str.strip, inp))
    data: dict[str, list[tuple[str, bool, int, str]]] = {}
    i: int = 0
    while inp[i]:
        workflow: str = inp[i]
        key: str = workflow.split("{")[0]
        condition: str = workflow.split("{")[1][:-1]
        conditions: list[tuple[str, bool, int, str]] = []
        for part in condition.split(",")[:-1]:
            conditions.append((
                part[0],
                part[1] == "<",
                int(part[2:part.index(":")]),
                part[part.index(":") + 1:]
            ))
        conditions.append((
            "x",
            False,
            -1,
            condition.split(",")[-1]
        ))
        data[key] = conditions
        i += 1

    i += 1
    pieces: list[dict[str, int]] = []
    while i < len(inp):
        piece: str = inp[i]
        piece = piece.replace("=", ":").replace("x", "'x'").replace(
            "m", "'m'").replace("a", "'a'").replace("s", "'s'")
        pieces.append(eval(piece))
        i += 1

    return data, pieces


def check_piece(conditions: dict[str, list[tuple[str, bool, int, str]]], piece: dict[str, int], current: str = "in") -> bool:
    if current == "R":
        return False

    if current == "A":
        return True

    condition: list[tuple[str, bool, int, str]] = conditions[current]
    for check in condition:
        key: str
        comparison: bool
        value: int
        jump: str
        key, comparison, value, jump = check

        if piece[key] < value and comparison:
            return check_piece(conditions, piece, jump)

        if piece[key] > value and not comparison:
            return check_piece(conditions, piece, jump)

    raise ValueError("Oh crap!")


def check_piece_range(conditions: dict[str, list[tuple[str, bool, int, str]]], piece: Hypercuboids, current: str = "in") -> Hypercuboids:
    if current == "R":
        return Hypercuboids()

    if current == "A":
        return piece

    condition: list[tuple[str, bool, int, str]] = conditions[current]
    ret: Hypercuboids = Hypercuboids()
    cur_possibilities: Hypercuboids = piece.copy()
    for check in condition:
        key: str
        comparison: bool
        value: int
        jump: str
        key, comparison, value, jump = check

        x_range: Range = Range(1, 4000)
        y_range: Range = Range(1, 4000)
        z_range: Range = Range(1, 4000)
        w_range: Range = Range(1, 4000)

        lower: int = 0
        upper: int = 4000
        if comparison:
            lower = value
        else:
            upper = value

        cut: Range = Range(lower, upper)

        if key == "x":
            x_range = cut
        if key == "m":
            y_range = cut
        if key == "a":
            z_range = cut
        if key == "s":
            w_range = cut

        removal_hypercuboid: Hypercuboid = Hypercuboid(
            x_range,
            y_range,
            z_range,
            w_range
        )

        path_possibilities: Hypercuboids = cur_possibilities.copy()
        path_possibilities.remove_hypercuboid(removal_hypercuboid)

        cur_possibilities.intersect(removal_hypercuboid)

        ret.add_hypercuboids(check_piece_range(
            conditions,
            path_possibilities,
            jump
        ))

    return ret


def main_part_1(inp: list[str]) -> OUTPUT_TYPE:
    condition, pieces = parse_inp(inp)

    ret: int = 0
    for piece in pieces:
        if check_piece(condition, piece):
            ret += sum(piece.values())

    return ret


def main_part_2(inp: list[str]) -> OUTPUT_TYPE:
    conditions, _ = parse_inp(inp)

    base_hypercuboid: Hypercuboids = Hypercuboids()
    base_hypercuboid.add_hypercuboid(Hypercuboid(
        Range(1, 4000),
        Range(1, 4000),
        Range(1, 4000),
        Range(1, 4000)
    ))

    return check_piece_range(
        conditions,
        base_hypercuboid,
    ).volume()


def main() -> None:
    test_input: str = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""
    test_input_parsed: list[str] = test_input.split("\n")
    test_output_part_1_expected: OUTPUT_TYPE = 19114
    test_output_part_2_expected: OUTPUT_TYPE = 167409079868000

    file_location: str = "Day 19/input.txt"
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
