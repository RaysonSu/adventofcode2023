from collections import defaultdict
OUTPUT_TYPE = int


def parse_inp(inp: list[str]) -> defaultdict[str, list[str]]:
    ret: defaultdict[str, set[str]] = defaultdict(lambda: set().copy())

    for i in inp:
        ret[i.split(": ")[0]] = ret[i.split(": ")[0]].union(
            set(i.split(": ")[1].strip().split(" ")))
        for j in i.split(": ")[1].strip().split(" "):
            ret[j].add(i.split(": ")[0])

    return ret


def main_part_1(inp: list[str]) -> OUTPUT_TYPE:
    q: defaultdict[str, list[str]] = inp.copy()
    inp = parse_inp(inp)

    components: list[str] = set(inp.keys())
    counts: defaultdict[str, int] = defaultdict(lambda: 0)

    for i in components:
        paths: defaultdict[str, set[str]] = defaultdict(lambda: set())
        seen: set[str] = set()
        latest: set[str] = {i}
        while latest:
            l_temp: set[str] = set()
            seen = seen.union(latest)
            for j in latest:
                for k in inp[j]:
                    if k in seen:
                        continue

                    l_temp.add(k)
                    paths[k] = paths[j].union({f"{j}/{k}", f"{k}/{j}"})

            latest = l_temp

        for i in paths.values():
            for j in i:
                counts[j] += 1

    banned: list[str] = [key for key, _ in sorted(list(
        counts.items()), key=lambda x: x[-1], reverse=True)[:6]]

    seen = set()
    latest = {q[0][:3]}
    while latest:
        l_temp = set()
        seen = seen.union(latest)
        for j in latest:
            for k in inp[j]:
                if k in seen:
                    continue

                path = f"{j}/{k}"
                if path in banned:
                    continue

                l_temp.add(k)

        latest = l_temp

    return len(seen) * (len(components) - len(seen))


def main() -> None:
    test_input: str = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr"""
    test_input_parsed: list[str] = test_input.split("\n")
    test_output_part_1_expected: OUTPUT_TYPE = 54

    file_location: str = "Day 25/input.txt"
    input_file: list[str] = open(file_location, "r").readlines()

    test_output_part_1: OUTPUT_TYPE = main_part_1(test_input_parsed)

    if test_output_part_1_expected == test_output_part_1:
        print(f"Part 1: {main_part_1(input_file)}")
    else:
        print(f"Part 1 testing error: ")
        print(f"Test input: {test_input}")
        print(f"Expected output: {test_output_part_1_expected}")
        print(f"Got: {test_output_part_1}")
        print()


if __name__ == "__main__":
    main()
