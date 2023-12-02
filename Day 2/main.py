OUTPUT_TYPE = int


def parse_inp(inp: list[str]) -> list[list[int]]:
    ret: list[list[int]] = []
    for game_data in inp:
        game: list[str] = game_data.split(":")
        game_id: int = int(game[0][5:])
        colors: list[int] = [0, 0, 0]

        for hand in game[1].split(";"):
            hand = hand.replace(",", "").strip()
            data: list[str] = hand.split(" ")

            for index in range(len(data)):
                if data[index] not in ["red", "green", "blue"]:
                    continue

                color: int = ["red", "green", "blue"].index(data[index])
                colors[color] = max(colors[color], int(data[index - 1]))

        ret.append([game_id, colors[0], colors[1], colors[2]])
    return ret


def main_part_1(inp: list[str]) -> OUTPUT_TYPE:
    parsed_input: list[list[int]] = parse_inp(inp)
    ret: int = 0

    for game in parsed_input:
        if game[1] <= 12 and game[2] <= 13 and game[3] <= 14:
            ret += game[0]

    return ret


def main_part_2(inp: list[str]) -> OUTPUT_TYPE:
    parsed_input: list[list[int]] = parse_inp(inp)
    ret: int = 0

    for game in parsed_input:
        ret += game[1] * game[2] * game[3]

    return ret


def main() -> None:
    test_input: str = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""
    test_input_parsed: list[str] = test_input.split("\n")
    test_output_part_1_expected: OUTPUT_TYPE = 8
    test_output_part_2_expected: OUTPUT_TYPE = 2286

    file_location: str = "Day 2/input.txt"
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
