def part1(input_txt: str) -> int:
    with open(input_txt) as f:
        lines = map(lambda x: x.strip(), f.readlines())
        matrix = [[int(c) for c in line] for line in lines]
        dirs = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        res = 0
        for col in range(len(matrix)):
            for row in range(len(matrix[0])):
                v = matrix[col][row]
                for d in dirs:
                    vis = True
                    col_n = col + d[0]
                    row_n = row + d[1]
                    while 0 <= col_n < len(matrix) and 0 <= row_n < len(matrix[0]):
                        if matrix[col_n][row_n] >= v:
                            vis = False
                            break
                        col_n += d[0]
                        row_n += d[1]
                    if vis:
                        res += 1
                        break
        return res


def part2(input_txt: str) -> int:
    return 0


if __name__ == "__main__":
    p1_ans = part1("input.txt")
    print(f"part1: {p1_ans}")
    p2_ans = part2("input.txt")
    print(f"part2: {p2_ans}")
