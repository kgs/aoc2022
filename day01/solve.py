def part1(input_txt):
    with open(input_txt) as f:
        lines = map(lambda x: x.strip(), f.readlines())
        best = 0
        tmp = 0
        for l in lines:
            if l == '':
                best = max(best, tmp)
                tmp = 0
            else:
                tmp += int(l)
        return best


def part2(input_txt):
    with open(input_txt) as f:
        lines = map(lambda x: x.strip(), f.readlines())
        s = []
        tmp = 0
        for l in lines:
            if l == '':
                s.append(tmp)
                tmp = 0
            else:
                tmp += int(l)
        return sum(sorted(s)[-3::])


if __name__ == "__main__":
    p1_ans = part1("part1.txt")
    print(f"part1: {p1_ans}")
    p2_ans = part2("part1.txt")
    print(f"part2: {p2_ans}")
