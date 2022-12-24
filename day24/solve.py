from typing import Iterable

from dataclasses import dataclass
from collections import deque

MAX_MINUTES = 1_000

DIRS = {
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0)
}

MoveVector = tuple[int, int]
Coord = tuple[int, int]
OccupiedSet = set[Coord]


@dataclass(frozen=True)
class Blizzard:
    x: int
    y: int
    vec: MoveVector


@dataclass
class Map:
    size_x: int
    size_y: int
    start: Coord
    end: Coord
    blizzards: list[Blizzard]

    def blizzard_at_minute(self, b: Blizzard, minute: int) -> Coord:
        x = (b.x + minute * b.vec[0]) % self.size_x
        y = (b.y + minute * b.vec[1]) % self.size_y
        return x, y


@dataclass(frozen=True)
class Position:
    minute: int
    coord: Coord


def calc_occupied_at_min(m: Map, minute: int) -> OccupiedSet:
    ret = set()
    for b in m.blizzards:
        ret.add(m.blizzard_at_minute(b, minute))
    return ret


def find_dot(line: str) -> int:
    return [x for x, v in enumerate(line) if v == '.'][0]


def parse_map(input_txt: str) -> Map:
    with open(input_txt) as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
        size_y = len(lines) - 2
        size_x = len(lines[0]) - 2
        start = (find_dot(lines[0][1:-1]), -1)
        end = (find_dot(lines[-1][1:-1]), size_y)
        blizzards = [
            Blizzard(x, y, DIRS[v]) for y, line in enumerate(lines[1:-1]) for x, v in enumerate(line[1:-1]) if v != "."
        ]
        return Map(size_x, size_y, start, end, blizzards)


def generate_moves(m: Map, p: Position, occupied_at_min: list[OccupiedSet]) -> Iterable[Position]:
    minute = p.minute + 1
    occupied = occupied_at_min[minute]
    for d in DIRS.values():
        nx = p.coord[0] + d[0]
        ny = p.coord[1] + d[1]
        if ((nx, ny) == m.end) or (0 <= nx < m.size_x and 0 <= ny < m.size_y and not (nx, ny) in occupied):
            yield Position(minute, (nx, ny))
    if p.coord not in occupied:
        yield Position(minute, p.coord)  # wait move


def walk(m: Map, minute: int, occupied_at_min: list[OccupiedSet]) -> int:
    curr_pos = Position(minute, m.start)
    q = deque([curr_pos])
    states = {curr_pos}
    while len(q):
        curr_pos = q.popleft()
        states.remove(curr_pos)
        if curr_pos.coord == m.end:
            return curr_pos.minute
        for pos in generate_moves(m, curr_pos, occupied_at_min):
            if pos not in states:
                q.append(pos)
                states.add(pos)

    raise Exception("should not happen!")


def solve(input_txt: str) -> tuple[int, int]:
    m = parse_map(input_txt)

    occupied_at_min = []
    for i in range(MAX_MINUTES):
        occupied_at_min.append(calc_occupied_at_min(m, i))

    first_min = walk(m, 0, occupied_at_min)
    m.start, m.end = m.end, m.start
    back_min = walk(m, first_min, occupied_at_min)
    m.start, m.end = m.end, m.start
    again_min = walk(m, back_min, occupied_at_min)

    return first_min, again_min


if __name__ == "__main__":
    sample_p1_ans, sample_p2_ans = solve("sample.txt")
    print(f"sample: {sample_p1_ans} {sample_p2_ans}")
    p1_ans, p2_ans = solve("input.txt")
    print(f"input: {p1_ans} {p2_ans}")
