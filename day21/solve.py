import operator

ROOT = "root"
HUMAN = "humn"

OPS = {
    "+": operator.add,
    "-": operator.sub,
    "/": operator.floordiv,
    "*": operator.mul
}

TREE = dict[str, tuple | None]


def parse_tree(input_txt: str) -> TREE:
    with open(input_txt) as f:
        tree = {}
        for line in f.readlines():
            tokens = line.split()
            match tokens:
                case [z, x, op, y]:
                    tree[z[:-1]] = (op, x, y)
                case [z, v]:
                    tree[z[:-1]] = (int(v))
        return tree


def calc(tree: TREE, node: str) -> int | None:
    match tree[node]:
        case (op, x, y):
            xv = calc(tree, x)
            yv = calc(tree, y)
            if xv is None or yv is None:
                return None
            return OPS[op](xv, yv)
        case (v):
            return v


def calc_human_value(tree: TREE, node: str, expected_result: int) -> int:
    match tree[node]:
        case (op, x, y):
            xv = calc(tree, x)
            yv = calc(tree, y)
            if xv is None:
                assert yv is not None
                # ??(x) <op> y == expected_result
                match op:
                    case "-":
                        return calc_human_value(tree, x, expected_result + yv)
                    case "+":
                        return calc_human_value(tree, x, expected_result - yv)
                    case "*":
                        return calc_human_value(tree, x, expected_result // yv)
                    case "/":
                        return calc_human_value(tree, x, expected_result * yv)
            elif yv is None:
                assert xv is not None
                # x <op> ??(y) == expected_result
                match op:
                    case "-":
                        return calc_human_value(tree, y, xv - expected_result)
                    case "+":
                        return calc_human_value(tree, y, expected_result - xv)
                    case "*":
                        return calc_human_value(tree, y, expected_result // xv)
                    case "/":
                        return calc_human_value(tree, y, xv // expected_result)
            else:
                assert False, "exactly one child should be None"
        case (v) if v is None:
            return expected_result
        case (v):
            assert False, "real leafs should not be reached"


def part1(input_txt: str) -> int:
    tree = parse_tree(input_txt)
    return calc(tree, ROOT)


def part2(input_txt: str) -> int:
    tree = parse_tree(input_txt)
    _, x, y = tree[ROOT]
    tree[ROOT] = ("-", x, y)  # x - y == 0
    tree[HUMAN] = None
    return calc_human_value(tree, ROOT, 0)


if __name__ == "__main__":
    sample_p1_ans = part1("sample.txt")
    assert sample_p1_ans == 152
    p1_ans = part1("input.txt")
    assert p1_ans == 282285213953670
    sample_p2_ans = part2("sample.txt")
    assert sample_p2_ans == 301
    p2_ans = part2("input.txt")
    assert p2_ans == 3699945358564
