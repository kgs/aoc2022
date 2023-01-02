from dataclasses import dataclass
from functools import reduce


@dataclass
class Monkey:
    id: int
    items: list[int]
    operation: str
    divisible: int
    throw_if_true: int
    throw_if_false: int


def parse_monkeys(input_txt: str) -> list[Monkey]:
    with open(input_txt) as f:
        monkeys_str = f.read().split("\n\n")
        monkeys = []
        for i, m_str in enumerate(monkeys_str):
            m_str = m_str.splitlines()
            items = list(map(int, m_str[1].split(":")[1].split(",")))
            operation = m_str[2].split("=")[1].strip()
            divisible = int(m_str[3].split()[3])
            throw_if_true = int(m_str[4].split()[5])
            throw_if_false = int(m_str[5].split()[5])
            monkeys.append(Monkey(i, items, operation, divisible, throw_if_true, throw_if_false))
        return monkeys


def part1(input_txt: str) -> int:
    monkeys = parse_monkeys(input_txt)
    active = [0] * len(monkeys)
    for _ in range(20):
        for m in monkeys:
            for item in m.items:
                item = eval(m.operation, {"old": item})
                item = item // 3
                if item % m.divisible == 0:
                    monkeys[m.throw_if_true].items.append(item)
                else:
                    monkeys[m.throw_if_false].items.append(item)
            active[m.id] += len(m.items)
            m.items = []
    active.sort(reverse=True)
    return active[0] * active[1]


def nwd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


def nww(a: int, b: int) -> int:
    return a * b // nwd(a, b)


def part2(input_txt: str) -> int:
    monkeys = parse_monkeys(input_txt)
    modulo = reduce(nww, [m.divisible for m in monkeys], 1)
    active = [0] * len(monkeys)
    for r in range(10_000):
        for m in monkeys:
            for item in m.items:
                item = eval(m.operation, {"old": item}) % modulo
                if item % m.divisible == 0:
                    monkeys[m.throw_if_true].items.append(item)
                else:
                    monkeys[m.throw_if_false].items.append(item)
            active[m.id] += len(m.items)
            m.items = []
    active.sort(reverse=True)
    return active[0] * active[1]


if __name__ == "__main__":
    sample_p1_ans = part1("sample.txt")
    print(f"sample1: {sample_p1_ans}")
    p1_ans = part1("input.txt")
    print(f"part1: {p1_ans}")
    sample_p2_ans = part2("sample.txt")
    print(f"sample2: {sample_p2_ans}")
    assert sample_p2_ans == 2713310158
    p2_ans = part2("input.txt")
    assert p2_ans == 19457438264
    print(f"part2: {p2_ans}")
