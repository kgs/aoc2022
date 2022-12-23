from pydantic.dataclasses import dataclass
from typing import Self
import re


@dataclass
class Tile:
    x: int
    y: int
    val: str


@dataclass
class Vector:
    vx: int
    vy: int

    def rotated_left(self) -> Self:
        return Vector(self.vy, -self.vx)

    def rotated_right(self) -> Self:
        return Vector(-self.vy, self.vx)

    def opposite(self) -> Self:
        return Vector(-self.vx, -self.vy)


DIRS = {
    "R": Vector(1, 0),
    "L": Vector(-1, 0),
    "U": Vector(0, -1),
    "D": Vector(0, 1)
}

VEC_POINTS = {
    (1, 0): 0,
    (0, 1): 1,
    (-1, 0): 2,
    (0, -1): 3
}


@dataclass
class Move:
    vec: Vector
    steps: int


def parse_maze(maze_str: str) -> list[list[Tile]]:
    lines = maze_str.splitlines()
    max_length = max([len(l) for l in lines])
    lines = [" " * max_length] + lines + [" " * max_length]  # sentinel line at first row and last row
    for i in range(len(lines)):
        lines[i] = " " + lines[i] \
                   + " " * (max_length - len(lines[i]) + 1)  # sentinel at start and many at end
    return [[Tile(x, y, val) for x, val in enumerate(line)] for y, line in enumerate(lines)]


def parse_moves(moves_str: str) -> list[Move]:
    tokens = re.split("([RL])", moves_str)
    d = DIRS["R"]
    moves = [Move(d, int(tokens[0]))]
    for i in range(1, len(tokens), 2):
        rotate = tokens[i]
        steps = int(tokens[i + 1])
        match rotate:
            case "R":
                d = d.rotated_right()
            case "L":
                d = d.rotated_left()
        moves.append(Move(d, steps))
    return moves


def find_start(maze: list[list[Tile]]) -> Tile:
    for t in maze[1]:  # first line == sentinels
        if t.val == '.':
            return t


def next_tile(maze: list[list[Tile]], curr_tile: Tile, vec: Vector) -> Tile:
    nx = curr_tile.x + vec.vx
    ny = curr_tile.y + vec.vy
    # if off the board, then wrap
    if maze[ny][nx].val == " ":
        opposite_vec = vec.opposite()
        while True:
            nx += opposite_vec.vx
            ny += opposite_vec.vy
            if maze[ny][nx].val == " ":
                # we are one step too far, move back
                nx += vec.vx
                ny += vec.vy
                break
    new_tile = maze[ny][nx]
    if new_tile.val == "#":
        return curr_tile
    elif new_tile.val == ".":
        return new_tile
    else:
        raise Exception("should not happen!")


def part1(input_txt: str) -> int:
    with open(input_txt) as f:
        maze_str, moves_str = f.read().split("\n\n")
        maze = parse_maze(maze_str)
        moves = parse_moves(moves_str)
        curr_tile = find_start(maze)
        for move in moves:
            for _ in range(move.steps):
                curr_tile = next_tile(maze, curr_tile, move.vec)
        last_vec = moves[-1].vec
        return 1000 * curr_tile.y + 4 * curr_tile.x + VEC_POINTS[(last_vec.vx, last_vec.vy)]


def part2(input_txt: str) -> int:
    with open(input_txt) as f:
        return 0


if __name__ == "__main__":
    sample_p1_ans = part1("sample.txt")
    assert sample_p1_ans == 6032
    p1_ans = part1("input.txt")
    assert p1_ans == 133174
    sample_p2_ans = part2("sample.txt")
    print(f"sample: {sample_p2_ans}")
    p2_ans = part2("input.txt")
    print(f"part2: {p2_ans}")
