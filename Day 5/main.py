from __future__ import annotations

OUTPUT_TYPE = int


class Ranges:  # stole this code from last year!
    def __init__(self, *ranges: tuple[int, int]) -> None:
        self.ranges: list[tuple[int,  int]] = []
        for number_range in ranges:
            self.ranges.append(number_range)

        self.fix_everything()

    def __str__(self) -> str:
        return str(self.ranges)

    def clean_up(self) -> None:
        while self.one_step_clean_up():
            pass

    def one_step_clean_up(self) -> bool:
        for range_index in range(len(self.ranges)):
            for other_range_index in range(range_index):
                new = self.combine(
                    self.ranges[range_index],
                    self.ranges[other_range_index]
                )
                if len(new) == 1:
                    self.ranges.pop(range_index)
                    self.ranges.pop(other_range_index)
                    self.ranges.append(new[0])
                    return True
        return False

    def remove_invalid_ranges(self) -> None:
        self.ranges = [
            number_range
            for number_range
            in self.ranges
            if number_range[1] >= number_range[0]
        ]

    def combine(self, interval_1: tuple[int, int], interval_2: tuple[int, int]) -> list[tuple[int, int]]:
        if interval_1[0] < interval_2[0]:
            if interval_1[1] < interval_2[0]:
                return [interval_1, interval_2]
            elif interval_2[1] <= interval_1[1]:
                return [interval_1]
            else:
                return [(interval_1[0], interval_2[1])]
        elif interval_1[0] == interval_2[0]:
            return [(interval_1[0], max(interval_1[1], interval_2[1]))]
        else:
            return self.combine(interval_2, interval_1)

    def sort(self) -> None:
        from functools import cmp_to_key

        def compare(left: tuple[int, int], right: tuple[int, int]):
            if right[1] <= left[0]:
                return 1
            else:
                return -1

        self.ranges.sort(key=cmp_to_key(compare))

    def fix_everything(self) -> None:
        self.remove_invalid_ranges()
        self.clean_up()
        self.sort()

    def length(self) -> int:
        return sum(upper - lower + 1 for upper, lower in self.ranges)

    def add(self, *ranges: Ranges | tuple[int, int]) -> None:
        for number_range in ranges:
            if isinstance(number_range, Ranges):
                for sub_interval in number_range.ranges:
                    self.ranges.append(sub_interval)
            elif isinstance(number_range, tuple):
                self.ranges.append(number_range)

        self.fix_everything()

    def remove(self, removal_interval: tuple[int, int]) -> Ranges:
        new_ranges: list[tuple[int, int]] = []
        removed_ranges: list[tuple[int, int]] = []
        for interval in self.ranges:
            if interval[1] <= removal_interval[1] and interval[0] >= removal_interval[0]:
                removed_ranges.append(interval)

            elif interval[1] > removal_interval[1] and interval[0] < removal_interval[0]:
                new_ranges.append((interval[0], removal_interval[0] - 1))
                new_ranges.append((removal_interval[1] + 1, interval[1]))
                removed_ranges.append(removal_interval)

            elif interval[1] <= removal_interval[1] and interval[1] >= removal_interval[0]:
                new_ranges.append((interval[0], removal_interval[0] - 1))
                removed_ranges.append((removal_interval[0], interval[1]))

            elif interval[0] >= removal_interval[0] and interval[0] <= removal_interval[1]:
                new_ranges.append((removal_interval[1] + 1, interval[1]))
                removed_ranges.append((interval[0], removal_interval[1]))

            else:
                new_ranges.append(interval)

        self.ranges = new_ranges

        ret: Ranges = Ranges()
        for interval in removed_ranges:
            ret.add(interval)

        return ret

    def shift(self, amount: int) -> None:
        new_ranges: list[tuple[int, int]] = []
        for start, end in self.ranges:
            new_ranges.append((start + amount, end + amount))
        self.ranges = new_ranges


def main_part_1(inp: list[str]) -> OUTPUT_TYPE:
    seeds: Ranges = Ranges()
    new_seeds: Ranges = Ranges()
    initial_seeds: list[str] = inp[0][7:].split()
    for i in range(len(initial_seeds)):
        seeds.add((
            int(initial_seeds[i]),
            int(initial_seeds[i])
        ))

    for line in inp[1:]:
        line = line.strip()

        if line == "":
            for seed in seeds.ranges:
                new_seeds.add(seed)
            seeds = new_seeds
            new_seeds = Ranges()
            continue

        if not line.replace(" ", "").isnumeric():
            continue

        values: list[int] = list(map(int, line.split()))
        removed: Ranges = seeds.remove((values[1], values[1] + values[2] - 1))
        removed.shift(values[0] - values[1])
        new_seeds.add(removed)

    seeds.add(new_seeds)

    return seeds.ranges[0][0]


def main_part_2(inp: list[str]) -> OUTPUT_TYPE:
    seeds: Ranges = Ranges()
    new_seeds: Ranges = Ranges()
    initial_seed_ranges: list[str] = inp[0][7:].split()
    for i in range(len(initial_seed_ranges) // 2):
        seeds.add((
            int(initial_seed_ranges[2 * i]),
            int(initial_seed_ranges[2 * i]) +
            int(initial_seed_ranges[2 * i + 1]) - 1
        ))

    for line in inp[1:]:
        line = line.strip()

        if line == "":
            for seed in seeds.ranges:
                new_seeds.add(seed)
            seeds = new_seeds
            new_seeds = Ranges()
            continue

        if not line.replace(" ", "").isnumeric():
            continue

        values: list[int] = list(map(int, line.split()))
        removed: Ranges = seeds.remove((values[1], values[1] + values[2] - 1))
        removed.shift(values[0] - values[1])
        new_seeds.add(removed)

    seeds.add(new_seeds)

    return seeds.ranges[0][0]


def main() -> None:
    test_input: str = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""
    test_input_parsed: list[str] = test_input.split("\n")
    test_output_part_1_expected: OUTPUT_TYPE = 35
    test_output_part_2_expected: OUTPUT_TYPE = 46

    file_location: str = "Day 5/input.txt"
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
