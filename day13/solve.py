from dataclasses import dataclass
from functools import cmp_to_key


@dataclass
class Packets:
    a: list
    b: list


def parse_packets(input_txt) -> list[Packets]:
    with open(input_txt) as f:
        pairs_str = f.read().split("\n\n")
        ret = []
        for ps in pairs_str:
            a, b = map(eval, ps.split())
            ret.append(Packets(a, b))
        return ret


def compare(a: list, b: list) -> int:
    match a, b:
        case [], []:
            return 0
        case [], [_, *_]:
            return -1
        case [_, *_], []:
            return 1
        case [int(hl), *tl], [int(hr), *tr]:
            if hl < hr:
                return -1
            elif hl > hr:
                return 1
            else:
                return compare(tl, tr)
        case [list(hl), *tl], [int(hr), *tr]:
            return compare([hl, *tl], [[hr], *tr])
        case [int(hl), *tl], [list(hr), *tr]:
            return compare([[hl], *tl], [hr, *tr])
        case [list(hl), *tl], [list(hr), *tr]:
            match compare(hl, hr):
                case 0:
                    return compare(tl, tr)
                case order:
                    return order


def part1(input_txt: str) -> int:
    packets = parse_packets(input_txt)
    return sum([idx + 1 for idx, p in enumerate(packets) if compare(p.a, p.b) == -1])


def part2(input_txt: str) -> int:
    packets = parse_packets(input_txt)
    all_packets = [x for p in packets for x in [p.a, p.b]]
    a, b = [[2]], [[6]]
    all_packets += [a, b]
    all_sorted = sorted(all_packets, key=cmp_to_key(compare))
    ia, ib = all_sorted.index(a), all_sorted.index(b)
    return (ia + 1) * (ib + 1)


if __name__ == "__main__":
    sample_p1_ans = part1("sample.txt")
    print(f"sample1: {sample_p1_ans}")
    p1_ans = part1("input.txt")
    print(f"part1: {p1_ans}")
    sample_p2_ans = part2("sample.txt")
    print(f"sample2: {sample_p2_ans}")
    p2_ans = part2("input.txt")
    print(f"part2: {p2_ans}")
