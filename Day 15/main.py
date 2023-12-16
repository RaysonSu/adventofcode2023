OUTPUT_TYPE = int


def hash_str(string: str) -> int:
    ret: int = 0
    for i in string:
        ret += ord(i)
        ret *= 17
        ret %= 256
    return ret


def main_part_1(inp: list[str]) -> OUTPUT_TYPE:
    return sum(map(hash_str, inp[0].split(",")))


def main_part_2(inp: list[str]) -> OUTPUT_TYPE:
    boxes: list[list[str]] = [[] for _ in range(256)]
    powers: dict[str, int] = {}

    for instruction in inp[0].split(","):
        lens: str
        location: int

        if instruction[-1] == "-":
            lens = instruction[:-1]
            location = hash_str(lens)
            if lens in boxes[location]:
                boxes[location].remove(lens)
        else:
            data: list[str] = instruction.split("=")
            lens = data[0]
            location = hash_str(lens)
            if lens not in boxes[location]:
                boxes[location].append(lens)
            powers[lens] = int(data[1])

    ret: int = 0
    for box_num, box in enumerate(boxes, 1):
        for lens_num, lens in enumerate(box, 1):
            ret += box_num * lens_num * powers[lens]

    return ret


def main() -> None:
    test_input: str = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""
    test_input_parsed: list[str] = test_input.split("\n")
    test_output_part_1_expected: OUTPUT_TYPE = 1320
    test_output_part_2_expected: OUTPUT_TYPE = 145

    file_location: str = "Day 15/input.txt"
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
