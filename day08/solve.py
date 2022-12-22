DIRS = [(0, 1), (1, 0), (-1, 0), (0, -1)]


def parse_matrix(input_txt: str) -> (list[list[int]], int, int):
    with open(input_txt) as f:
        lines = map(lambda x: x.strip(), f.readlines())
        matrix = [[int(c) for c in line] for line in lines]
        return matrix, len(matrix), len(matrix[0])  # matrix, cols, rows


def part1(input_txt: str) -> int:
    matrix, num_cols, num_rows = parse_matrix(input_txt)
    res = 0
    for col in range(num_cols):
        for row in range(num_rows):
            v = matrix[col][row]
            for d in DIRS:
                vis = True
                col_n = col + d[0]
                row_n = row + d[1]
                while 0 <= col_n < num_cols and 0 <= row_n < num_rows:
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
    matrix, num_cols, num_rows = parse_matrix(input_txt)
    best = 0
    for col in range(num_cols):
        for row in range(num_rows):
            v = matrix[col][row]
            res = 1
            for d in DIRS:
                e = 0
                col_n = col + d[0]
                row_n = row + d[1]
                while 0 <= col_n < num_cols and 0 <= row_n < num_rows:
                    e += 1
                    if matrix[col_n][row_n] >= v:
                        break
                    col_n += d[0]
                    row_n += d[1]
                res *= e
            best = max(best, res)
    return best


if __name__ == "__main__":
    p1_ans = part1("input.txt")
    print(f"part1: {p1_ans}")
    p2_ans = part2("input.txt")
    print(f"part2: {p2_ans}")
