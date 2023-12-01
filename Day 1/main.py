def get_digit(string: str, replacer: list[str], reverse: bool) -> str:
    for index in range(len(string)):
        target_index: int = (-index - 1) if reverse else index
        if string[target_index].isnumeric():
            return string[target_index]

        for digit, name in enumerate(replacer):
            if (not reverse and string[index:].startswith(name)) \
                    or (reverse and string[:len(string) - index].endswith(name)):
                return str(digit)

    return ""


def main_part_1(inp: list[str]) -> int:
    ret: int = 0
    for line in inp:
        first: str = get_digit(line, replacer=[], reverse=False)
        last: str = get_digit(line, replacer=[], reverse=True)
        ret += int(first + last)
    return ret


def main_part_2(inp: list[str]) -> int:
    replacer: list[str] = ["zero", "one", "two", "three",
                           "four", "five", "six", "seven", "eight", "nine"]
    ret: int = 0

    for line in inp:
        line = line.strip()
        first: str = get_digit(line, replacer, False)
        last: str = get_digit(line, replacer, True)
        ret += int(first + last)
    return ret


def main() -> None:
    file_location: str = "Day 1/input.txt"
    input_file: list[str] = open(file_location, "r").readlines()
    print(main_part_1(input_file))
    print(main_part_2(input_file))


if __name__ == "__main__":
    main()
