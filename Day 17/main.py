from __future__ import annotations
import heapq


OUTPUT_TYPE = int


class State:
    def __init__(self, grid: list[str], low: int, high: int, location: tuple[int, int] = (0, 0), prev: tuple[int, int] = (0, 0), cont: int = 100000000):
        self.grid: list[str] = grid
        self.location: tuple[int, int] = location
        self.low: int = low
        self.high: int = high
        self.prev: tuple[int, int] = prev
        self.cont: int = cont

    def generate_neighbours(self) -> list[tuple[int, State]]:
        ret: list[tuple[int, State]] = []

        for direction in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            if self.cont < self.low and direction != self.prev:  # disallows turning if not enough
                continue

            if direction[0] == -self.prev[0] and direction[1] == -self.prev[1]:  # bans reversing
                continue

            new_cont: int
            if direction == self.prev:
                new_cont = self.cont + 1
            else:
                new_cont = 1

            if new_cont > self.high:  # prevents going too far in a direction
                continue

            new_location: tuple[int, int] = (
                self.location[0] + direction[0],
                self.location[1] + direction[1]
            )

            # checks that it's a valid location
            if not self.is_valid_coord(new_location):
                continue

            cost: int = int(self.grid[new_location[1]][new_location[0]])

            ret.append((cost, State(self.grid, self.low, self.high,
                       new_location, direction, new_cont)))

        return ret

    def is_valid_coord(self, location: tuple[int, int]) -> bool:
        if location[0] < 0 or location[0] >= len(self.grid[0]):
            return False

        if location[1] < 0 or location[1] >= len(self.grid):
            return False

        return True

    def is_finished(self) -> bool:
        if self.location != (len(self.grid[0]) - 1, len(self.grid) - 1):
            return False

        if self.cont < self.low:
            return False

        if self.cont > self.high:
            return False

        return True

    def __hash__(self) -> int:
        return hash(f"{self.location}//{self.prev}//{self.cont}")

    def __lt__(self, other) -> bool:
        return hash(self) < hash(other)


def main_part_1(inp: list[str]) -> OUTPUT_TYPE:
    inp = list(map(str.strip, inp))
    initial_state: State = State(inp, 1, 3)
    best_found: dict[int, int] = {hash(initial_state): 0}
    states: list[tuple[int, State]] = [(0, initial_state)]

    while states:
        current_score: int
        current_state: State

        current_score, current_state = heapq.heappop(states)

        if current_state.is_finished():
            return current_score

        for cost, new_state in current_state.generate_neighbours():
            new_cost: int = current_score + cost
            hashed_state: int = hash(new_state)

            if hashed_state in best_found.keys() and best_found[hashed_state] <= new_cost:
                continue

            best_found[hashed_state] = new_cost
            heapq.heappush(states, (new_cost, new_state))

    return -1


def main_part_2(inp: list[str]) -> OUTPUT_TYPE:
    inp = list(map(str.strip, inp))
    initial_state: State = State(inp, 4, 10)
    best_found: dict[int, int] = {hash(initial_state): 0}
    states: list[tuple[int, State]] = [(0, initial_state)]

    while states:
        current_score: int
        current_state: State

        current_score, current_state = heapq.heappop(states)

        if current_state.is_finished():
            return current_score

        for cost, new_state in current_state.generate_neighbours():
            new_cost: int = current_score + cost
            hashed_state: int = hash(new_state)

            if hashed_state in best_found.keys() and best_found[hashed_state] <= new_cost:
                continue

            best_found[hashed_state] = new_cost
            heapq.heappush(states, (new_cost, new_state))

    return -1


def main() -> None:
    test_input: str = """111111111111
999999999991
999999999991
999999999991
999999999991"""
    test_input_parsed: list[str] = test_input.split("\n")
    test_output_part_1_expected: OUTPUT_TYPE = 59
    test_output_part_2_expected: OUTPUT_TYPE = 71

    file_location: str = "Day 17/input.txt"
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
