from __future__ import annotations
from collections import deque, defaultdict

OUTPUT_TYPE = int


class State:
    def __init__(self, grid: list[str], location: tuple[int, int], time: int = 0, forced: int = -1, visited: set[tuple[int, int]] | None = set(), ignore: bool = False) -> None:
        self.grid: list[str] = grid
        self.location: tuple[int, int] = location
        self.time: int = time
        self.forced: int = forced
        if visited:
            self.visited: set[tuple[int, int]] = visited
        else:
            self.visited = set()
        self.ignore: bool = ignore
        self.visited.add(location)

    def neighbours(self) -> list[State]:
        ret: list[State] = []
        if self.grid[self.location[1]][self.location[0]] == "#":
            return []

        for direction in range(4):
            if self.forced != -1 and direction != self.forced:
                continue

            new_location: tuple[int, int] = (
                self.location[0] + [1, 0, -1, 0][direction],
                self.location[1] + [0, -1, 0, 1][direction]
            )

            if new_location[1] < 0:
                continue

            if new_location[1] >= len(self.grid):
                continue

            if new_location in self.visited:
                continue
            try:
                tile: str = self.grid[new_location[1]][new_location[0]]
            except IndexError as _:
                continue

            if tile == "#":
                continue

            forced: int = -1
            if tile in ">^<v" and not self.ignore:
                forced = ">^<v".index(tile)

            new_visited: set[tuple[int, int]] = self.visited.copy()
            new_visited.add(new_location)

            ret.append(State(
                self.grid,
                new_location,
                self.time + 1,
                forced,
                new_visited,
                self.ignore
            ))

        return ret

    def copy(self) -> State:
        return State(
            self.grid,
            self.location,
            self.time,
            self.forced,
            self.visited
        )

    def __hash__(self) -> int:
        return hash(str(self.location))


class State_abstract:
    def __init__(self, paths: dict[tuple[int, int], tuple[int, tuple[int, int]]],
                 location: tuple[int, int],
                 time: int = 0,
                 visited: set[tuple[int, int]] = set()) -> None:
        self.paths: dict[tuple[int, int], tuple[int, tuple[int, int]]] = paths
        self.location: tuple[int, int] = location
        self.time: int = time
        self.visited: set[tuple[int, int]] = visited
        self.visited.add(location)

    def neighbours(self) -> list[State_abstract]:
        ret: list[tuple[int, State_abstract]] = []
        for direction in range(4):
            cost: int
            new_location: tuple[int, int]
            cost, new_location = self.paths[self.location][direction]

            if new_location == (-1, -1):
                continue

            if new_location in self.visited:
                continue

            new_visited: set[tuple[int, int]] = self.visited.copy()
            new_visited.add(new_location)

            ret.append(State_abstract(
                self.paths,
                new_location,
                self.time + cost,
                new_visited
            ))

        return ret


def distance(grid: list[int], source: tuple[int, int], goals: list[tuple[int, int]], direction: int) -> tuple[int, tuple[int, int]]:
    states: deque[State] = deque()
    states.append(State(grid, source, forced=direction, ignore=True))
    while states:
        active: State = states.popleft()
        neighbours: list[State] = active.neighbours()
        if active.location in goals and active.location != source:
            return active.time, active.location

        for neighbour in neighbours:
            states.append(neighbour)

    return -1, (-1, -1)


def main_part_1(inp: list[str]) -> OUTPUT_TYPE:
    inp = list(map(str.strip, inp))
    states: deque[State] = deque()
    states.append(State(inp, (1, 0)))
    best_dist: defaultdict[tuple[int, int], int] = defaultdict(lambda: 0)
    best: int = 0
    while states:
        active: State = states.popleft()
        neighbours: list[State] = active.neighbours()
        if active.location == (len(inp[0]) - 2, len(inp) - 1):
            best = max(best, active.time)

        for neighbour in neighbours:
            if best_dist[neighbour.location] > neighbour.time:
                continue

            best_dist[neighbour.location] = neighbour.time
            states.append(neighbour)

    return best


def main_part_2(inp: list[str]) -> OUTPUT_TYPE:
    inp = list(map(str.strip, inp))

    points: list[tuple[int, int]] = []
    for row_index in range(1, len(inp) - 1):
        for col_index in range(1, len(inp[0]) - 1):
            chars: str = inp[row_index][col_index - 1] \
                + inp[row_index][col_index + 1] \
                + inp[row_index - 1][col_index] \
                + inp[row_index + 1][col_index]

            if "." not in chars and inp[row_index][col_index] == ".":
                points.append((col_index, row_index))
    points.insert(0, (1, 0))
    points.append((len(inp[0]) - 2, len(inp) - 1))

    point_path: dict[tuple[int, int], tuple[int, tuple[int, int]]]
    point_path = {
        point: [(-1, (-1, -1)) for _ in range(4)]
        for point in points
    }

    for key in point_path.keys():
        for i in range(4):
            point_path[key][i] = distance(inp, key, points, i)

    states: deque[State_abstract] = deque()
    states.append(State_abstract(point_path, (1, 0)))
    best: int = 0
    while states:
        active: State_abstract = states.popleft()
        neighbours: list[State] = active.neighbours()
        if active.location == (len(inp[0]) - 2, len(inp) - 1):
            best = max(best, active.time)

        for neighbour in neighbours:
            states.append(neighbour)

        print("\r", len(states), best, "   ", end="")

    return best


def main() -> None:
    test_input: str = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...# 
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""
    test_input_parsed: list[str] = test_input.split("\n")
    test_output_part_1_expected: OUTPUT_TYPE = 94
    test_output_part_2_expected: OUTPUT_TYPE = 154

    file_location: str = "Day 23/input.txt"
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
