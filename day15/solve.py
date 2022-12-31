import re

Sensor = tuple[int, int, int]


def manhattan(x1: int, y1: int, x2: int, y2: int) -> int:
    return abs(x1 - x2) + abs(y1 - y2)


def generate_coords_in_row(sensors: list[Sensor], y: int) -> list[tuple[int, int]]:
    coords = []
    for s in sensors:
        xs, ys, d = s
        dy = abs(ys - y)
        if dy <= d:
            left_x = xs + dy - d
            right_x = d - dy + xs
            coords += [(left_x, 0), (right_x, 1)]
    coords.sort()
    return coords


def calc_taken_in_row(sensors: list[Sensor], y: int) -> int:
    coords = generate_coords_in_row(sensors, y)
    res = 0
    overlapping = 0
    start = None
    for c in coords:
        if c[1] == 0:
            # start of interval
            overlapping += 1
            if overlapping == 1:
                start = c[0]
        elif c[1] == 1:
            # end of interval
            overlapping -= 1
            if overlapping == 0:
                res += c[0] - start + 1
    return res


def part1(input_txt: str, row: int) -> int:
    with open(input_txt) as f:
        sensors = []
        beacons = set()
        for line in f.readlines():
            sx, sy, bx, by = map(int, re.findall(r"-?\d+", line))
            beacons.add((bx, by))
            sensors.append((sx, sy, manhattan(sx, sy, bx, by)))
        beacons_in_row = len([y for _, y in beacons if y == row])
        return calc_taken_in_row(sensors, row) - beacons_in_row


def get_free_x_in_row(sensors: list[Sensor], y: int, max_x: int) -> int | None:
    coords = generate_coords_in_row(sensors, y)
    overlapping = 0
    if len(coords) > 0:
        if coords[0][0] - 1 >= 0:
            return coords[0][0] - 1
    for c in coords:
        if c[1] == 0:
            # start of interval
            overlapping += 1
        elif c[1] == 1:
            # end of interval
            overlapping -= 1
            if overlapping == 0:
                # we have candidate
                if c[0] + 1 <= max_x:
                    return c[0] + 1
    return None


def part2(input_txt: str, max_xy: int) -> int:
    with open(input_txt) as f:
        sensors = []
        for line in f.readlines():
            sx, sy, bx, by = map(int, re.findall(r"-?\d+", line))
            sensors.append((sx, sy, manhattan(sx, sy, bx, by)))
        for y in range(max_xy):
            x = get_free_x_in_row(sensors, y, max_xy)
            if x is not None:
                return x * 4000000 + y


if __name__ == "__main__":
    sample_p1_ans = part1("sample.txt", 10)
    print(f"sample1: {sample_p1_ans}")
    p1_ans = part1("input.txt", 2000000)
    print(f"part1: {p1_ans}")
    sample_p2_ans = part2("sample.txt", 20)
    print(f"sample2: {sample_p2_ans}")
    p2_ans = part2("input.txt", 4000000)
    print(f"part2: {p2_ans}")
