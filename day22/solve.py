from pydantic.dataclasses import dataclass
from typing import Self
import re
import types


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


Direction = types.SimpleNamespace()  # to be used as constant in match-case
Direction.RIGHT = Vector(1, 0)
Direction.LEFT = Vector(-1, 0)
Direction.UP = Vector(0, -1)
Direction.DOWN = Vector(0, 1)

VEC_POINTS = {
    (1, 0): 0,
    (0, 1): 1,
    (-1, 0): 2,
    (0, -1): 3
}


@dataclass
class Move:
    rotate: str | None
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
    moves = [Move(None, int(tokens[0]))]
    for i in range(1, len(tokens), 2):
        rotate = tokens[i]
        steps = int(tokens[i + 1])
        moves.append(Move(rotate, steps))
    return moves


def find_start(maze: list[list[Tile]]) -> Tile:
    for t in maze[1]:  # first line == sentinels
        if t.val == '.':
            return t


def next_tile(maze: list[list[Tile]], curr_tile: Tile, vec: Vector) -> tuple[Tile, Vector]:
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
        return curr_tile, vec
    elif new_tile.val == ".":
        return new_tile, vec
    else:
        raise Exception("should not happen!")


def update_vec(vec: Vector, move: Move) -> Vector:
    match move.rotate:
        case "L":
            vec = vec.rotated_left()
        case "R":
            vec = vec.rotated_right()
    return vec


def calc_points(curr_tile: Tile, curr_vec: Vector) -> int:
    return 1000 * curr_tile.y + 4 * curr_tile.x + VEC_POINTS[(curr_vec.vx, curr_vec.vy)]


def part1(input_txt: str) -> int:
    with open(input_txt) as f:
        maze_str, moves_str = f.read().split("\n\n")
        maze = parse_maze(maze_str)
        moves = parse_moves(moves_str)
        curr_tile = find_start(maze)
        curr_vec = Direction.RIGHT
        for move in moves:
            curr_vec = update_vec(curr_vec, move)
            for _ in range(move.steps):
                curr_tile, curr_vec = next_tile(maze, curr_tile, curr_vec)
        return calc_points(curr_tile, curr_vec)


def face_3d(x: int, y: int) -> tuple[int, tuple[int, int, int, int]]:
    # x1, x2, y1, y2
    # sentinels included!
    faces = [
        (9, 9 + 4, 1, 1 + 4),
        (1, 1 + 4, 5, 5 + 4),
        (5, 5 + 4, 5, 5 + 4),
        (9, 9 + 4, 5, 5 + 4),
        (9, 9 + 4, 9, 9 + 4),
        (13, 13 + 4, 9, 9 + 4)
    ]
    for i, f in enumerate(faces):
        x1, x2, y1, y2 = f
        if x1 <= x < x2 and y1 <= y < y2:
            return i + 1, faces[i]
    raise Exception("should not happen!")


def move_to_zero(x: int, y: int, face_coords: tuple[int, int, int, int]) -> tuple[int, int]:
    return x - face_coords[0], y - face_coords[2]


def move_from_zero(x: int, y: int, face_coords: tuple[int, int, int, int]) -> tuple[int, int]:
    return x + face_coords[0], y + face_coords[2]


def rotate_right_via_zero(x: int, y: int) -> tuple[int, int]:
    # we are rotating point which represents top-left coord of tile
    # so, after rotating via (0, 0) we need to add -1 to x-coord to make it top-left again
    return -y - 1, x


def rotate_and_move(x: int, y: int, vec, right_rotations: int,
                    x_moves: int, y_moves: int) -> tuple[int, int, Vector]:
    _, face_coords = face_3d(x, y)
    face_size = face_coords[1] - face_coords[0]
    assert face_size == (face_coords[3] - face_coords[2])
    # given some border tile (x, y) on some face, rotate it and move it to be close to new face
    # vector is also rotated, so applying it to new (x, y) will make it inside new face
    x, y = move_to_zero(x, y, face_coords)
    for _ in range(right_rotations):
        x, y = rotate_right_via_zero(x, y)
        x += face_size
        vec = vec.rotated_right()
    x, y = move_from_zero(x, y, face_coords)
    x += x_moves * face_size
    y += y_moves * face_size
    return x, y, vec


def transition_from_border(x: int, y: int, vec: Vector) -> tuple[int, int, Vector]:
    curr_face, _ = face_3d(x, y)
    res = None
    match curr_face:
        case 1:
            match vec:
                case Direction.LEFT:  # 3
                    res = rotate_and_move(x, y, vec, 3, -1, 0)
                case Direction.RIGHT:  # 6
                    res = rotate_and_move(x, y, vec, 2, 2, 2)
                case Direction.UP:  # 2
                    res = rotate_and_move(x, y, vec, 2, -2, 0)
        case 2:
            match vec:
                case Direction.LEFT:  # 6
                    res = rotate_and_move(x, y, vec, 1, 3, 2)
                case Direction.UP:  # 1
                    res = rotate_and_move(x, y, vec, 2, 2, -2)
                case Direction.DOWN:  # 5
                    res = rotate_and_move(x, y, vec, 2, 2, 2)
        case 3:
            match vec:
                case Direction.UP:  # 1
                    res = rotate_and_move(x, y, vec, 1, 0, -1)
                case Direction.DOWN:  # 5
                    res = rotate_and_move(x, y, vec, 3, 0, 1)
        case 4:
            match vec:
                case Direction.RIGHT:  # 6
                    res = rotate_and_move(x, y, vec, 1, 1, 0)
        case 5:
            match vec:
                case Direction.LEFT:  # 3
                    res = rotate_and_move(x, y, vec, 1, -1, 0)
                case Direction.DOWN:  # 2
                    res = rotate_and_move(x, y, vec, 2, -2, 0)
        case 6:
            match vec:
                case Direction.UP:  # 4
                    res = rotate_and_move(x, y, vec, 3, 0, -1)
                case Direction.RIGHT:  # 1
                    res = rotate_and_move(x, y, vec, 2, 0, -2)
                case Direction.DOWN:  # 2
                    res = rotate_and_move(x, y, vec, 3, -4, -1)
    if res is None:
        raise Exception("should not happen!")
    x, y, vec = res
    # make move into new face before returning
    return x + vec.vx, y + vec.vy, vec


def next_tile_3d(maze: list[list[Tile]], curr_tile: Tile, vec: Vector) -> tuple[Tile, Vector]:
    nx = curr_tile.x + vec.vx
    ny = curr_tile.y + vec.vy
    new_vec = vec
    # if off the board, then transition to other cube face
    if maze[ny][nx].val == " ":
        nx, ny, new_vec = transition_from_border(curr_tile.x, curr_tile.y, vec)
    new_tile = maze[ny][nx]
    if new_tile.val == "#":
        return curr_tile, vec
    elif new_tile.val == ".":
        return new_tile, new_vec
    else:
        raise Exception("should not happen!")


def part2(input_txt: str) -> int:
    with open(input_txt) as f:
        maze_str, moves_str = f.read().split("\n\n")
        maze = parse_maze(maze_str)
        moves = parse_moves(moves_str)
        curr_tile = find_start(maze)
        curr_vec = Direction.RIGHT
        for move in moves:
            curr_vec = update_vec(curr_vec, move)
            for _ in range(move.steps):
                curr_tile, curr_vec = next_tile_3d(maze, curr_tile, curr_vec)
        return calc_points(curr_tile, curr_vec)


def test():
    assert rotate_and_move(9, 2, Direction.LEFT, 3, -1, 0) == (6, 4, Direction.DOWN)
    assert transition_from_border(12, 6, Direction.RIGHT) == (15, 9, Direction.DOWN)
    assert transition_from_border(11, 12, Direction.DOWN) == (2, 8, Direction.UP)


if __name__ == "__main__":
    test()
    sample_p1_ans = part1("sample.txt")
    assert sample_p1_ans == 6032
    p1_ans = part1("input.txt")
    assert p1_ans == 133174
    sample_p2_ans = part2("sample.txt")
    print(f"sample: {sample_p2_ans}")
    # p2_ans = part2("input.txt")
    # print(f"part2: {p2_ans}")
