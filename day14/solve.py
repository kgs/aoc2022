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


def simulate_sand(c: Cave, start: tuple[int, int]) -> bool:
    curr_pos = start
    while True:
        next_pos = curr_pos
        if c.taken[next_pos[1] + 1][next_pos[0]] == 0:
            next_pos = (next_pos[0], next_pos[1] + 1)
        elif c.taken[next_pos[1] + 1][next_pos[0] - 1] == 0:
            next_pos = (next_pos[0] - 1, next_pos[1] + 1)
        elif c.taken[next_pos[1] + 1][next_pos[0] + 1] == 0:
            next_pos = (next_pos[0] + 1, next_pos[1] + 1)
        if curr_pos == next_pos:
            # cannot move, place on cave
            c.taken[next_pos[1]][next_pos[0]] = 2
            return True
        else:
            # move
            curr_pos = next_pos
        if curr_pos[1] > c.max_y_taken:
            # falling down infinitely...
            return False


def part1(input_txt: str) -> int:
    cave = parse_cave(input_txt)
    start = (500, 0)
    res = 0
    while simulate_sand(cave, start):
        res += 1
    return res


def part2(input_txt: str) -> int:
    return 0


if __name__ == "__main__":
    sample_p1_ans = part1("sample.txt")
    print(f"sample1: {sample_p1_ans}")
    p1_ans = part1("input.txt")
    print(f"part1: {p1_ans}")
    sample_p2_ans = part2("sample.txt")
    print(f"sample2: {sample_p2_ans}")
    p2_ans = part2("input.txt")
    print(f"part2: {p2_ans}")
