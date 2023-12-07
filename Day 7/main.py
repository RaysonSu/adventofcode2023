from functools import cmp_to_key
OUTPUT_TYPE = int


def measure_hand(hand: str) -> int:
    unique_cards: int = len(set(hand))
    max_card_count: int = max([hand.count(card) for card in hand])
    if unique_cards == 1:
        return 7

    if unique_cards == 2:
        if max_card_count == 4:
            return 6

        return 5

    if unique_cards == 3:
        if max_card_count == 3:
            return 4

        return 3

    if unique_cards == 4:
        return 2

    return 1


def measure_hand_J(x: str) -> int:
    best: int = 0
    for replacement in "AKQT98765432":
        best = max(best, measure_hand(x.replace("J", replacement)))
    return best


def compare_hands_simple(hand_1: list[str], hand_2: list[str]) -> int:
    hand_1_cards: str = hand_1[0]
    hand_2_cards: str = hand_2[0]
    if measure_hand(hand_1_cards) > measure_hand(hand_2_cards):
        return 1
    if measure_hand(hand_2_cards) > measure_hand(hand_1_cards):
        return -1
    for card_1, card_2, in zip(hand_1_cards, hand_2_cards):
        card_order: str = "AKQJT98765432"
        if card_order.index(card_1) > card_order.index(card_2):
            return -1
        if card_order.index(card_2) > card_order.index(card_1):
            return 1
    return 0


def compare_hands_complex(hand_1: list[str], hand_2: list[str]) -> int:
    hand_1_cards: str = hand_1[0]
    hand_2_cards: str = hand_2[0]
    if measure_hand_J(hand_1_cards) > measure_hand_J(hand_2_cards):
        return 1
    if measure_hand_J(hand_2_cards) > measure_hand_J(hand_1_cards):
        return -1
    for card_1, card_2, in zip(hand_1_cards, hand_2_cards):
        card_order: str = "AKQT98765432J"
        if card_order.index(card_1) > card_order.index(card_2):
            return -1
        if card_order.index(card_2) > card_order.index(card_1):
            return 1
    return 0


def main_part_1(inp: list[str]) -> OUTPUT_TYPE:
    ret: int = 0
    parsed_inp: list[list[str]] = [hand.split() for hand in inp if hand != ""]
    parsed_inp.sort(key=cmp_to_key(compare_hands_simple))
    for index, hand in enumerate(parsed_inp, 1):
        ret += int(hand[1]) * index
    return ret


def main_part_2(inp: list[str]) -> OUTPUT_TYPE:
    ret: int = 0
    parsed_inp: list[list[str]] = [hand.split() for hand in inp if hand != ""]
    parsed_inp.sort(key=cmp_to_key(compare_hands_complex))
    for index, hand in enumerate(parsed_inp, 1):
        ret += int(hand[1]) * index
    return ret


def main() -> None:
    test_input: str = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""
    test_input_parsed: list[str] = test_input.split("\n")
    test_output_part_1_expected: OUTPUT_TYPE = 6440
    test_output_part_2_expected: OUTPUT_TYPE = 5905

    file_location: str = "python/Advent of Code/2023/Day 7/input.txt"
    input_file: list[str] = open(file_location, "r").readlines()
    input_file = [x.replace("\n", "") for x in input_file]

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
