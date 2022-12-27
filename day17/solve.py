from dataclasses import field
from typing import Self
from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class Rock:
    blocks: list[tuple[int, int]]


@dataclass
class RockSequence:
    rocks: list[Rock] = field(default_factory=lambda: [
        Rock([(0, 0), (1, 0), (2, 0), (3, 0)]),
        Rock([(0, 1), (1, 1), (2, 1), (1, 0), (1, 2)]),
        Rock([(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]),
        Rock([(0, 0), (0, 1), (0, 2), (0, 3)]),
        Rock([(0, 0), (1, 0), (0, 1), (1, 1)])
    ])
    i: int = 0

    def next_rock(self) -> Rock:
        res = self.rocks[self.i]
        self.i += 1
        self.i %= len(self.rocks)
        return res


@dataclass
class PushSequence:
    s: str
    i: int = 0

    def next_x_push(self) -> int:
        res = -1 if self.s[self.i] == "<" else 1
        self.i += 1
        self.i %= len(self.s)
        return res


@dataclass
class Board:
    # first row is 1 (0 is sentinel floor) and they grow UP, every row has 7-bools + 2 sentinels
    rows: list[list[bool]] = field(default_factory=lambda: [[True] * (7 + 2)])
    last_filled_row: int = 0
    rocks_count: int = 0

    def ensure_enough_free_rows(self):
        # 3 free rows + 4 rows for biggest rock
        missing_rows = self.last_filled_row + 1 + 3 + 4 - len(self.rows)
        if missing_rows > 0:
            for _ in range(missing_rows):
                row = [True] + [False] * 7 + [True]
                self.rows.append(row)

    def put_rock(self, rock: "MovingRock"):
        for pos in rock.blocks_pos:
            x, y = pos
            assert self.rows[y][x] is False
            self.rows[y][x] = True
            self.last_filled_row = max(self.last_filled_row, y)
        self.rocks_count += 1

    def print(self):
        for i, row in enumerate(reversed(self.rows)):
            print(str(len(self.rows) - 1 - i), "".join(["#" if c else "." for c in row]))


@dataclass
class MovingRock:
    blocks_pos: list[tuple[int, int]]

    def jet_push(self, x_diff: int, b: Board):
        for pos in self.blocks_pos:
            x, y = pos
            if b.rows[y][x + x_diff]:
                return
        for i in range(len(self.blocks_pos)):
            x, y = self.blocks_pos[i]
            self.blocks_pos[i] = (x + x_diff, y)

    def fall(self, b: Board) -> bool:
        for pos in self.blocks_pos:
            x, y = pos
            if b.rows[y - 1][x]:
                return False
        for i in range(len(self.blocks_pos)):
            x, y = self.blocks_pos[i]
            self.blocks_pos[i] = (x, y - 1)
        return True

    @classmethod
    def init_on_board(cls, rock: Rock, b: Board) -> Self:
        x, y = 3, b.last_filled_row + 4
        blocks_pos = [(x + pos[0], y + pos[1]) for pos in rock.blocks]
        return cls(blocks_pos)


def simulate(b: Board, push_seq: PushSequence, rock_seq: RockSequence, rounds: int, stop_row: int | None) -> Board:
    for r in range(rounds):
        b.ensure_enough_free_rows()
        rock = MovingRock.init_on_board(rock_seq.next_rock(), b)
        falling = True
        while falling:
            rock.jet_push(push_seq.next_x_push(), b)
            falling = rock.fall(b)
        b.put_rock(rock)
        if stop_row and b.last_filled_row >= stop_row:
            return b
    return b


def part1(input_txt: str) -> int:
    with open(input_txt) as f:
        b = Board()
        push_seq = PushSequence(f.read().strip())
        rock_seq = RockSequence()
        b = simulate(b, push_seq, rock_seq, 2022, None)
        return b.last_filled_row


def find_cycle(b: Board, max_start_pos: int, max_cycle_len: int) -> tuple[int, int]:
    for cycle_start in range(1, max_start_pos):
        for cycle_length in range(10, max_cycle_len):
            if b.rows[cycle_start:cycle_start + cycle_length] == \
                    b.rows[cycle_start + cycle_length: cycle_start + cycle_length * 2]:
                return cycle_start, cycle_length


def part2(input_txt: str) -> int:
    with open(input_txt) as f:
        push_str = f.read().strip()
        rounds = 1000000000000
        rounds_for_cycle = 7_000
        b = simulate(Board(), PushSequence(push_str), RockSequence(), rounds_for_cycle, None)
        cycle_start, cycle_length = find_cycle(b, 1_000, 5_000)

        b = Board()
        push_seq = PushSequence(push_str)
        rock_seq = RockSequence()
        b = simulate(b, push_seq, rock_seq, rounds_for_cycle, cycle_start)
        cycle_start = b.last_filled_row
        cycle_start_rounds = b.rocks_count
        b = simulate(b, push_seq, rock_seq, rounds_for_cycle, cycle_start + cycle_length)
        cycle_length_rounds = b.rocks_count - cycle_start_rounds

        rounds -= cycle_start_rounds
        cycle_count, rounds_left = divmod(rounds, cycle_length_rounds)

        rows_before_last_run = b.last_filled_row
        b = simulate(b, push_seq, rock_seq, rounds_left, None)
        last_run_rows = b.last_filled_row - rows_before_last_run
        return cycle_start + cycle_count * cycle_length + last_run_rows


if __name__ == "__main__":
    sample_p1_ans = part1("sample.txt")
    print(f"sample1: {sample_p1_ans}")
    p1_ans = part1("input.txt")
    print(f"part1: {p1_ans}")
    sample_p2_ans = part2("sample.txt")
    print(f"sample2: {sample_p2_ans}")
    p2_ans = part2("input.txt")
    print(f"part2: {p2_ans}")
