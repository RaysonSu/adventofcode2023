OUTPUT_TYPE = int


def parse_inp(inp: list[str]) -> None:
    return


def energised(inp: list[str], initial: tuple[int, int, int]) -> int:
    beams: list[tuple[int, int, int]] = [initial]
    engerized: set[tuple[int, int]] = set()
    seen_beams: set[tuple[int, int, int]] = set()
    while beams:
        new_beams: list[tuple[int, int, int]] = []
        for beam in beams:
            new_loc: tuple[int, int] = (
                beam[0] + [1, 0, -1, 0][beam[2]],
                beam[1] + [0, -1, 0, 1][beam[2]]
            )

            if new_loc[0] < 0 or new_loc[0] >= len(inp[0]) or new_loc[1] < 0 or new_loc[1] >= len(inp):
                continue

            tile = inp[new_loc[1]][new_loc[0]]

            new_directions: list[int] = []
            if tile == ".":
                new_directions.append(beam[2])
            elif tile == "\\":
                new_directions.append(3 - beam[2])
            elif tile == "/":
                new_directions.append([1, 0, 3, 2][beam[2]])
            elif tile == "-":
                if beam[2] in [0, 2]:
                    new_directions.append(beam[2])
                else:
                    new_directions.append(0)
                    new_directions.append(2)
            elif tile == "|":
                if beam[2] in [1, 3]:
                    new_directions.append(beam[2])
                else:
                    new_directions.append(1)
                    new_directions.append(3)

            for direction in new_directions:
                new_beam: tuple[int, int, int] = new_loc + (direction,)
                if new_beam in seen_beams:
                    continue

                engerized.add(new_loc)
                seen_beams.add(new_beam)
                new_beams.append(new_beam)
        beams = new_beams

    return len(engerized)


def main_part_1(inp: list[str]) -> OUTPUT_TYPE:
    inp = [row.strip() for row in inp]
    return energised(inp, (-1, 0, 0))


def main_part_2(inp: list[str]) -> OUTPUT_TYPE:
    inp = [row.strip() for row in inp]
    ret: int = 0
    for i in range(len(inp)):
        ret = max(ret, energised(inp, (-1, i, 0)))
        ret = max(ret, energised(inp, (len(inp[0]), i, 2)))

    for i in range(len(inp[0])):
        ret = max(ret, energised(inp, (i, -1, 3)))
        ret = max(ret, energised(inp, (i, len(inp), 1)))
    return ret


def main() -> None:
    test_input: str = """.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\\
..../.\\\..
.-.-/..|..
.|....-|.\\
..//.|...."""
    test_input_parsed: list[str] = test_input.split("\n")
    test_output_part_1_expected: OUTPUT_TYPE = 46
    test_output_part_2_expected: OUTPUT_TYPE = 51

    file_location: str = "Day 16/input.txt"
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
