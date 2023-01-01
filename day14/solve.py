from dataclasses import dataclass, field

N = 1009


@dataclass
class Cave:
    segments: list[tuple[int, int, int, int]]
    taken: list[list[int]]
    max_y_taken: int


def parse_cave(input_txt) -> Cave:
    with open(input_txt) as f:
        segments = []
        for line in f.readlines():
            points_str = map(lambda x: x.strip(), line.split("->"))
            points = [s.split(",") for s in points_str]
            points = [(int(t[0]), int(t[1])) for t in points]
            for i in range(1, len(points)):
                a = points[i - 1]
                b = points[i]
                segments += [(*a, *b)]
        taken = [[0] * N for _ in range(N)]
        max_y = 0
        for seg in segments:
            x1, y1, x2, y2 = seg
            max_y = max(max_y, y1, y2)
            for x in range(min(x1, x2), max(x1, x2) + 1):
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    taken[y][x] = 1
        return Cave(segments, taken, max_y)


def simulate_sand(c: Cave, start_pos: tuple[int, int], infinite_fall: bool) -> bool:
    if c.taken[start_pos[1]][start_pos[0]]:
        # cannot move, start is blocked
        return False
    curr_pos = start_pos
    while True:
        next_pos = curr_pos
        if c.taken[next_pos[1] + 1][next_pos[0]] == 0:
            next_pos = (next_pos[0], next_pos[1] + 1)
        elif c.taken[next_pos[1] + 1][next_pos[0] - 1] == 0:
            next_pos = (next_pos[0] - 1, next_pos[1] + 1)
        elif c.taken[next_pos[1] + 1][next_pos[0] + 1] == 0:
            next_pos = (next_pos[0] + 1, next_pos[1] + 1)
        if infinite_fall and next_pos[1] > c.max_y_taken:
            # falling down infinitely...
            return False
        if curr_pos == next_pos or next_pos[1] == c.max_y_taken + 1:
            # cannot move, place on cave
            c.taken[next_pos[1]][next_pos[0]] = 2
            return True
        else:
            # move
            curr_pos = next_pos


def solve(input_txt: str, infinite_fall: bool) -> int:
    cave = parse_cave(input_txt)
    res = 0
    while simulate_sand(cave, (500, 0), infinite_fall):
        res += 1
    return res


if __name__ == "__main__":
    sample_p1_ans = solve("sample.txt", infinite_fall=True)
    print(f"sample1: {sample_p1_ans}")
    p1_ans = solve("input.txt", infinite_fall=True)
    print(f"part1: {p1_ans}")
    sample_p2_ans = solve("sample.txt", infinite_fall=False)
    print(f"sample2: {sample_p2_ans}")
    p2_ans = solve("input.txt", infinite_fall=False)
    print(f"part2: {p2_ans}")
