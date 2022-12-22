from pydantic.dataclasses import dataclass

DIRS = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, 1),
    "D": (0, -1)
}


@dataclass
class Point:
    x: int
    y: int

    def move(self, vx: int, vy: int):
        self.x += vx
        self.y += vy


def sign(x: int) -> int:
    return (x > 0) - (x < 0)


def is_touching(h: Point, t: Point) -> bool:
    return abs(h.x - t.x) <= 1 and abs(h.y - t.y) <= 1


def part1(input_txt: str) -> int:
    with open(input_txt) as f:
        lines = map(lambda x: x.strip(), f.readlines())
        h = Point(0, 0)
        t = Point(0, 0)
        visited = {(t.x, t.y)}
        for move in lines:
            where, steps = move.split()
            for s in range(int(steps)):
                vx, vy = DIRS[where]
                h.move(vx, vy)
                if not is_touching(h, t):
                    t.move(sign(h.x - t.x), sign(h.y - t.y))
                    visited.add((t.x, t.y))
        return len(visited)


def part2(input_txt: str) -> int:
    return 0


if __name__ == "__main__":
    p1_ans = part1("input.txt")
    print(f"part1: {p1_ans}")
    p2_ans = part2("input.txt")
    print(f"part2: {p2_ans}")
