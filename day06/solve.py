def solve(input_txt: str, n: int) -> int:
    with open(input_txt) as f:
        s = f.read()
        for i in range(n, len(s)):
            if len(set(s[i - n:i])) == n:
                return i


if __name__ == "__main__":
    sample_ans = solve("sample.txt", 4)
    assert sample_ans == 5
    p1_ans = solve("input.txt", 4)
    assert p1_ans == 1987
    p2_ans = solve("input.txt", 14)
    assert p2_ans == 3059
