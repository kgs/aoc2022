from dataclasses import dataclass
from typing import Self


@dataclass
class Node:
    v: int
    prev: Self
    next: Self

    def swap_forward(self):
        old_next = self.next
        old_prev = self.prev
        self.next = old_next.next
        self.prev = old_next
        old_next.next = self
        old_next.prev = old_prev
        # fix neighbours
        self.next.prev = self
        old_prev.next = old_next


def move(e: Node, steps: int):
    if steps > 0:
        for _ in range(steps):
            e.swap_forward()
    elif steps < 0:
        for _ in range(-steps):
            p = e.prev
            p.swap_forward()


def skip(e: Node, steps: int) -> Node:
    for _ in range(steps):
        e = e.next
    return e


def dump(e: Node) -> list[int]:
    start = e
    res = []
    while e.next != start:
        res.append(e.v)
        e = e.next
    res.append(e.v)
    return res


def parse_list(input_txt: str) -> list[int]:
    with open(input_txt) as f:
        return [int(x) for x in f.readlines()]


def calc_result(nodes):
    zero = next(e for e in nodes if e.v == 0)
    res = 0
    for _ in range(3):
        zero = skip(zero, 1000)
        res += zero.v
    return res


def prepare_nodes(values):
    nodes = [Node(values[0], None, None)]
    for i in range(1, len(values)):
        prev = nodes[i - 1]
        curr = Node(values[i], prev, None)
        nodes.append(curr)
        prev.next = curr
    nodes[-1].next = nodes[0]
    nodes[0].prev = nodes[-1]
    return nodes


def part1(input_txt: str) -> int:
    values = parse_list(input_txt)
    nodes = prepare_nodes(values)
    for n in nodes:
        move(n, n.v)
    return calc_result(nodes)


def part2(input_txt: str) -> int:
    values = [v * 811589153 for v in parse_list(input_txt)]
    nodes = prepare_nodes(values)
    for _ in range(10):
        for n in nodes:
            steps = n.v % (len(values) - 1)
            move(n, steps)
    return calc_result(nodes)


if __name__ == "__main__":
    sample_p1_ans = part1("sample.txt")
    print(f"sample1: {sample_p1_ans}")
    p1_ans = part1("input.txt")
    print(f"part1: {p1_ans}")
    sample_p2_ans = part2("sample.txt")
    print(f"sample2: {sample_p2_ans}")
    p2_ans = part2("input.txt")
    print(f"part2: {p2_ans}")
