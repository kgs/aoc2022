def points1(p1: int, p2: int) -> int:
    p = p2 + 1
    if p1 == p2:
        p += 3
    elif (p1 + 1) % 3 == p2:
        p += 6
    return p


def part1(input_txt: str) -> int:
    with open(input_txt) as f:
        lines = map(lambda x: x.strip(), f.readlines())
        res = 0
        for line in lines:
            a, b = line.split()
            p1 = ord(a) - ord('A')
            p2 = ord(b) - ord('X')
            res += points1(p1, p2)
        return res


def points2(p1: int, r: int) -> int:
    p = r * 3
    match r:
        case 2:
            p += (p1 + 1) % 3 + 1
        case 1:
            p += p1 + 1
        case 0:
            p += (p1 + 2) % 3 + 1
    return p


def part2(input_txt: str) -> int:
    with open(input_txt) as f:
        lines = map(lambda x: x.strip(), f.readlines())
        res = 0
        for line in lines:
            a, b = line.split()
            p1 = ord(a) - ord('A')
            r = ord(b) - ord('X')
            res += points2(p1, r)
        return res


if __name__ == "__main__":
    p1_ans = part1("part1.txt")
    print(f"part1: {p1_ans}")
    p2_ans = part2("part1.txt")
    print(f"part2: {p2_ans}")
