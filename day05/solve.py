from typing import Self
from dataclasses import field
from pydantic.dataclasses import dataclass
from collections import deque
from collections.abc import Iterator
import re


@dataclass
class Stack:
    value: deque[str] = field(default_factory=lambda: deque())

    def pop(self, count: int) -> Iterator[str]:
        for _ in range(count):
            yield self.value.pop()

    def pop_and_reverse(self, count: int) -> list[str]:
        ret = []
        for _ in range(count):
            ret.append(self.value.pop())
        return ret[::-1]

    def put(self, elem: str) -> None:
        self.value.append(elem)

    def peek(self) -> str:
        return self.value[-1]

    @classmethod
    def from_str(cls, s: str) -> Self:
        return cls(value=deque(s))


@dataclass
class Move:
    src: int
    dst: int
    count: int

    @classmethod
    def from_str(cls, s: str) -> Self:
        c, src, dst = map(int, re.findall(r"\d+", s))
        return cls(src=src - 1, dst=dst - 1, count=c)


def rotate_right(lines: list[str]) -> list[str]:
    len_y = len(lines)
    len_x = len(lines[0])
    rotated = [['' for _ in range(len_y)] for _ in range(len_x)]
    for i in range(len_x):
        for j in range(len_y):
            rotated[i][len_y - j - 1] = lines[j][i]
    res = ["".join(l) for l in rotated]
    return res


def extract_stack_lines(stacks_str: str) -> Iterator[str]:
    lines = stacks_str.split("\n")[:-1]  # get rid of last line with numbers
    rotated = rotate_right(lines)
    for l in rotated:
        l = l.strip()
        if l.isalpha():
            yield l


def parse_stacks_and_moves(s):
    stacks_str, moves_str = s.read().split("\n\n")
    stacks = list(map(Stack.from_str, extract_stack_lines(stacks_str)))
    moves = map(Move.from_str, moves_str.split("\n"))
    return stacks, moves


def part1(input_txt: str) -> str:
    with open(input_txt) as f:
        stacks, moves = parse_stacks_and_moves(f)
        for m in moves:
            for e in stacks[m.src].pop(m.count):
                stacks[m.dst].put(e)
        return "".join([s.peek() for s in stacks])


def part2(input_txt: str) -> str:
    with open(input_txt) as f:
        stacks, moves = parse_stacks_and_moves(f)
        for m in moves:
            for e in stacks[m.src].pop_and_reverse(m.count):
                stacks[m.dst].put(e)
        return "".join([s.peek() for s in stacks])


if __name__ == "__main__":
    p1_ans = part1("input.txt")
    print(f"part1: {p1_ans}")
    p2_ans = part2("input.txt")
    print(f"part2: {p2_ans}")
