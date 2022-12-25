DEC_DIGITS = {
    "=": -2,
    "-": -1,
    "0": 0,
    "1": 1,
    "2": 2,
}

SNAFU_DIGITS = "012=-"


def snafu2dec(s: str) -> int:
    return sum(DEC_DIGITS[c] * 5 ** i for i, c in enumerate(reversed(s)))


def dec2snafu(x: int) -> str:
    digits = []
    while x > 0:
        x, d = divmod(x, 5)
        digits.insert(0, d)
    res = []
    carry = 0
    for d in reversed(digits):
        v = d + carry
        carry = 0
        if v > 2:
            carry = 1
        res.append(SNAFU_DIGITS[v])
    if carry == 1:
        res.append(SNAFU_DIGITS[carry])
    return "".join(reversed(res))


def part1(input_txt: str) -> str:
    with open(input_txt) as f:
        lines = map(lambda v: v.strip(), f.readlines())
        x = sum(snafu2dec(l) for l in lines)
        return dec2snafu(x)


if __name__ == "__main__":
    sample_p1_ans = part1("sample.txt")
    assert sample_p1_ans == "2=-1=0"
    p1_ans = part1("input.txt")
    assert p1_ans == "2=1-=02-21===-21=200"
