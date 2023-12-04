OUTPUT_TYPE = int


def parse_inp(inp: list[str]) -> None:
    return


def main_part_1(inp: list[str]) -> OUTPUT_TYPE:
    ret: int = 0
    for card in inp:
        card_data: list[str] = card.split(":")[1].split("|")

        winning_numbers: list[str] = card_data[0].split(" ")
        winning_numbers = [number for number in winning_numbers if number]

        card_numbers: list[str] = card_data[1].split(" ")
        card_numbers = [number for number in card_numbers if number]

        numbers_won: int = 0
        for number in card_numbers:
            if number in winning_numbers:
                numbers_won += 1

        if numbers_won:
            ret += 2 ** (numbers_won - 1)
    return ret


def main_part_2(inp: list[str]) -> OUTPUT_TYPE:
    card_count: list[int] = [1 for _ in range(len(inp))]
    for card_id, card in enumerate(inp):
        card_data: list[str] = card.split(":")[1].split("|")

        winning_numbers: list[str] = card_data[0].split(" ")
        winning_numbers = [number for number in winning_numbers if number]

        card_numbers: list[str] = card_data[1].split(" ")
        card_numbers = [number for number in card_numbers if number]

        numbers_won: int = 0
        for number in card_numbers:
            if number in winning_numbers:
                numbers_won += 1

        for extra_card in range(numbers_won):
            if card_id + extra_card + 1 >= len(inp):
                continue

            extra_card_id = card_id + extra_card + 1
            card_count[extra_card_id] += card_count[card_id]
    return sum(card_count)


def main() -> None:
    test_input: str = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""
    test_input_parsed: list[str] = test_input.split("\n")
    test_output_part_1_expected: OUTPUT_TYPE = 13
    test_output_part_2_expected: OUTPUT_TYPE = 30

    file_location: str = "Day 4/input.txt"
    input_file: list[str] = open(file_location, "r").readlines()
    input_file = list(map(str.strip, input_file))

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
