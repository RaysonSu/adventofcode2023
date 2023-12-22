from collections import deque, defaultdict
from functools import reduce
from math import lcm
OUTPUT_TYPE = int


def find_sources(infulences: defaultdict[str, list[str]], target: str) -> list[str]:
    found: list[str] = []
    for key, value in infulences.items():
        if target in value:
            found.append(key)

    return found


def parse_inp(inp: list[str]) -> tuple[defaultdict[str, list[str]], defaultdict[str, str], defaultdict[str, int]]:
    ret: defaultdict[str, list[str]] = defaultdict(lambda: [].copy())
    types: defaultdict[str, str] = defaultdict(lambda: "-")
    count: defaultdict[str, int] = defaultdict(lambda: 0)
    for line in inp:
        module_type: str = "-"
        if line[0] in "&%":
            module_type = line[0]
            line = line[1:]

        data: list[str] = line.split(" -> ")
        module_id: str = data[0]
        data[1] = data[1].strip()
        location: list[str] = data[1].split(", ")
        ret[module_id] = location
        types[module_id] = module_type

    for line in inp:
        data = line.split(" -> ")
        data[1] = data[1].strip()
        location = data[1].split(", ")
        for loc in location:
            count[loc] += 1

    return ret, types, count


def main_part_1(inp: list[str]) -> OUTPUT_TYPE:
    infulences: defaultdict[str, list[str]]
    types: defaultdict[str, str]
    flip_flop_states: defaultdict[str, bool]
    conj_states: defaultdict[str, defaultdict[str, bool]]
    conj_counts: defaultdict[str, int]

    infulences, types, conj_counts = parse_inp(inp)
    flip_flop_states = defaultdict(lambda: False)
    conj_states = defaultdict(lambda: defaultdict(lambda: False))
    conj_seen: defaultdict[str, set[str]] = defaultdict(lambda: set())

    broadcast_chain: deque[tuple[str, str, bool]] = deque()
    low_pulses: int = 0
    high_pulses: int = 0
    for _ in range(1000):
        broadcast_chain.append(("broadcaster", "button", False))
        low_pulses += 1
        while broadcast_chain:
            active: str
            source: str
            signal: bool

            active, source, signal = broadcast_chain.popleft()

            if types[active] == "-":
                for item in infulences[active]:
                    broadcast_chain.append((item, active, False))
                    low_pulses += 1
                continue

            if types[active] == "%":
                if signal:
                    continue

                flip_flop_states[active] = not flip_flop_states[active]
                for item in infulences[active]:
                    broadcast_chain.append(
                        (item, active, flip_flop_states[active]))
                    if flip_flop_states[active]:
                        high_pulses += 1
                    else:
                        low_pulses += 1
                continue

            if types[active] == "&":
                conj_states[active][source] = signal
                conj_seen[active].add(source)

                product: bool = reduce(
                    lambda x, y: x and y, conj_states[active].values())

                product = product and len(
                    conj_seen[active]) == conj_counts[active]

                for item in infulences[active]:
                    broadcast_chain.append(
                        (item, active, not product))
                    if product:
                        low_pulses += 1
                    else:
                        high_pulses += 1

    return low_pulses * high_pulses


def main_part_2(inp: list[str]) -> OUTPUT_TYPE:
    infulences: defaultdict[str, list[str]]
    types: defaultdict[str, str]
    flip_flop_states: defaultdict[str, bool]
    conj_states: defaultdict[str, defaultdict[str, bool]]
    conj_counts: defaultdict[str, int]
    conj_seen: defaultdict[str, set[str]]

    infulences, types, conj_counts = parse_inp(inp)
    flip_flop_states = defaultdict(lambda: False)
    conj_states = defaultdict(lambda: defaultdict(lambda: False))
    conj_seen = defaultdict(lambda: set())

    rx_source: str = find_sources(infulences, "rx")[0]
    requirements: list[str] = find_sources(infulences, rx_source)
    period: dict[str, int] = {key: 0 for key in requirements}

    broadcast_chain: deque[tuple[str, str, bool]] = deque()
    count: int = 0
    while 0 in period.values():
        broadcast_chain.append(("broadcaster", "button", False))
        count += 1
        while broadcast_chain:
            active: str
            source: str
            signal: bool

            active, source, signal = broadcast_chain.popleft()

            if active == "rx" and not signal:
                return count

            if active == rx_source and signal:
                period[source] = count

            if types[active] == "-":
                for item in infulences[active]:
                    broadcast_chain.append((item, active, False))
                continue

            if types[active] == "%":
                if signal:
                    continue

                flip_flop_states[active] = not flip_flop_states[active]
                for item in infulences[active]:
                    broadcast_chain.append(
                        (item, active, flip_flop_states[active]))
                continue

            if types[active] == "&":
                conj_states[active][source] = signal
                conj_seen[active].add(source)

                product: bool = reduce(
                    lambda x, y: x and y, conj_states[active].values())

                product = product and len(
                    conj_seen[active]) == conj_counts[active]

                for item in infulences[active]:
                    broadcast_chain.append(
                        (item, active, not product))

    return reduce(lcm, period.values())


def main() -> None:
    test_input: str = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> rx"""
    test_input_parsed: list[str] = test_input.split("\n")
    test_output_part_1_expected: OUTPUT_TYPE = 11687500
    test_output_part_2_expected: OUTPUT_TYPE = 0

    file_location: str = "Day 20/input.txt"
    input_file: list[str] = open(file_location, "r").readlines()

    test_output_part_1: OUTPUT_TYPE = main_part_1(test_input_parsed)
    test_output_part_2: OUTPUT_TYPE = 0

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
