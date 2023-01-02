from collections import deque
from typing import Iterable

INF = 424242


def parse_map(input_txt) -> list[list[int]]:
    with open(input_txt) as f:
        m = []
        for line in f:
            row = [INF] + [ord(c) for c in line.strip()] + [INF]
            m.append(row)
        sentinels = [INF for _ in range(len(m[0]))]
        m = [sentinels] + m + [sentinels]
        return m


def find_pos(m: list[list[int]], v: int) -> Iterable[tuple[int, int]]:
    for y in range(len(m)):
        for x in range(len(m[0])):
            if m[y][x] == v:
                yield x, y


def steps(m: list[list[int]], start: list[tuple[int, int]], end: tuple[int, int]) -> int:
    dirs = [(0, -1), (-1, 0), (1, 0), (0, 1)]
    q = deque()
    for s in start:
        q.append((s, 0))
    visited = set()
    while q:
        e = q.popleft()
        pos, curr_steps = e
        if pos in visited:
            continue
        if pos == end:
            return curr_steps
        x, y = pos
        for d in dirs:
            nx = x + d[0]
            ny = y + d[1]
            if m[ny][nx] <= m[y][x] + 1:
                q.append(((nx, ny), curr_steps + 1))
        visited.add(pos)


def part1(input_txt: str) -> int:
    m = parse_map(input_txt)
    start = list(find_pos(m, ord('S')))[0]
    end = list(find_pos(m, ord('E')))[0]
    m[start[1]][start[0]] = ord('a')
    m[end[1]][end[0]] = ord('z')
    return steps(m, [start], end)


def part2(input_txt: str) -> int:
    m = parse_map(input_txt)
    start = list(find_pos(m, ord('S')))[0]
    end = list(find_pos(m, ord('E')))[0]
    m[start[1]][start[0]] = ord('a')
    m[end[1]][end[0]] = ord('z')
    start = list(find_pos(m, ord('a')))
    return steps(m, start, end)


if __name__ == "__main__":
    sample_p1_ans = part1("sample.txt")
    print(f"sample1: {sample_p1_ans}")
    p1_ans = part1("input.txt")
    print(f"part1: {p1_ans}")
    sample_p2_ans = part2("sample.txt")
    print(f"sample2: {sample_p2_ans}")
    p2_ans = part2("input.txt")
    print(f"part2: {p2_ans}")
