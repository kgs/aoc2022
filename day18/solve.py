from typing import Iterable
import sys

Point = tuple[int, int, int]


def parse_graph(input_txt: str) -> set[Point]:
    with open(input_txt) as f:
        return {tuple(map(int, x.split(","))) for x in f.readlines()}


def neighbours(p: Point) -> Iterable[Point]:
    diffs = [-1, 1]
    x, y, z = p
    for d in diffs:
        yield Point((x + d, y, z))
        yield Point((x, y + d, z))
        yield Point((x, y, z + d))


def part1(input_txt: str) -> int:
    g = parse_graph(input_txt)
    res = 0
    for p in g:
        res += 6
        for n in neighbours(p):
            if n in g:
                res -= 1
    return res


def flow_and_count(g: set[Point], visited: set[Point], p: Point, min_p: Point, max_p: Point) -> int:
    assert p not in g
    if not all(a <= b <= c for a, b, c in zip(min_p, p, max_p)):
        # we are out of bounds
        return 0
    if p in visited:
        return 0
    visited.add(p)
    res = 0
    for n in neighbours(p):
        if n in g:
            res += 1
        else:
            res += flow_and_count(g, visited, n, min_p, max_p)
    return res


def part2(input_txt: str) -> int:
    sys.setrecursionlimit(10_000)  # DFS could be non-recursive but who cares :P
    g = parse_graph(input_txt)
    min_point = Point(min(p[i] for p in g) - 1 for i in range(3))
    max_point = Point(max(p[i] for p in g) + 1 for i in range(3))
    # noinspection PyTypeChecker
    return flow_and_count(g, set(), min_point, min_point, max_point)


if __name__ == "__main__":
    sample_p1_ans = part1("sample.txt")
    print(f"sample1: {sample_p1_ans}")
    p1_ans = part1("input.txt")
    print(f"part1: {p1_ans}")
    sample_p2_ans = part2("sample.txt")
    print(f"sample2: {sample_p2_ans}")
    p2_ans = part2("input.txt")
    print(f"part2: {p2_ans}")
