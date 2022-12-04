from typing import Self
from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class Range:
    left: int
    right: int

    def contains_fully(self, other: Self) -> bool:
        return self.left <= other.left and other.right <= self.right

    def overlaps(self, other: Self) -> bool:
        return self.left <= other.right and other.left <= self.right

    @classmethod
    def from_str(cls, s: str) -> Self:
        # conversion to int not necessary here (pydantic will do that)
        return cls(*map(int, s.split("-")))


def part1(input_txt: str) -> int:
    with open(input_txt) as f:
        lines = map(lambda x: x.strip(), f.readlines())
        res = 0
        for line in lines:
            a, b = map(Range.from_str, line.split(","))
            res += int(a.contains_fully(b) or b.contains_fully(a))
        return res


def part2(input_txt: str) -> int:
    with open(input_txt) as f:
        lines = map(lambda x: x.strip(), f.readlines())
        res = 0
        for line in lines:
            a, b = map(Range.from_str, line.split(","))
            res += int(a.overlaps(b))
        return res


if __name__ == "__main__":
    p1_ans = part1("part1.txt")
    print(f"part1: {p1_ans}")
    p2_ans = part2("part1.txt")
    print(f"part2: {p2_ans}")
