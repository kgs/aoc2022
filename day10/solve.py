def part1(input_txt: str) -> int:
    with open(input_txt) as f:
        lines = map(lambda v: v.strip(), f.readlines())
        x = 1
        x_at_cycle = [x]
        for line in lines:
            tokens = line.split()
            match tokens:
                case ["noop"]:
                    x_at_cycle.append(x)
                case ["addx", val]:
                    x_at_cycle.append(x)
                    x_at_cycle.append(x)
                    x += int(val)

        return sum([x_at_cycle[i] * i for i in range(20, 221, 40)])


def part2(input_txt: str) -> int:
    with open(input_txt) as f:
        return 0


if __name__ == "__main__":
    p1_ans = part1("input.txt")
    print(f"part1: {p1_ans}")
    p2_ans = part2("input.txt")
    print(f"part2: {p2_ans}")
