def priority(c: str) -> int:
    if c.islower():
        return ord(c) - ord('a') + 1
    else:
        return ord(c) - ord('A') + 27


def part1(input_txt: str) -> int:
    with open(input_txt) as f:
        lines = map(lambda x: x.strip(), f.readlines())
        res = 0
        for line in lines:
            half = len(line) // 2
            a, b = set(line[:half]), set(line[half:])
            common = a & b
            res += priority(common.pop())
        return res


def part2(input_txt: str) -> int:
    with open(input_txt) as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
        res = 0
        for i in range(len(lines) // 3):
            a, b, c = set(lines[i * 3]), set(lines[i * 3 + 1]), set(lines[i * 3 + 2])
            common = a & b & c
            res += priority(common.pop())
        return res


if __name__ == "__main__":
    p1_ans = part1("part1.txt")
    print(f"part1: {p1_ans}")
    p2_ans = part2("part1.txt")
    print(f"part2: {p2_ans}")
