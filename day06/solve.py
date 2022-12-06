from collections import deque


def solve(input_txt: str, n: int) -> int:
    with open(input_txt) as f:
        s = f.read()
        d = deque(s[:n])
        for i, c in enumerate(s[n:]):
            d.popleft()
            d.append(c)
            if len(set(d)) == n:
                return i + n + 1


if __name__ == "__main__":
    p1_ans = solve("input.txt", 4)
    print(f"part1: {p1_ans}")
    p1_ans = solve("input.txt", 14)
    print(f"part1: {p1_ans}")
