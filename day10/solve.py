from pydantic.dataclasses import dataclass
from dataclasses import field


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


@dataclass
class Screen:
    pos: int = 0
    curr_line: str = ""
    result: list[str] = field(default_factory=list)

    def put(self, c: str):
        self.curr_line += c
        self.pos += 1
        if self.pos == 40:
            self.pos = 0
            self.result.append(self.curr_line)
            self.curr_line = ""

    def print(self):
        for line in self.result:
            print(line)


def draw(x: int, s: Screen):
    if abs(x - s.pos) <= 1:
        s.put("#")
    else:
        s.put(".")


def part2(input_txt: str):
    with open(input_txt) as f:
        lines = map(lambda v: v.strip(), f.readlines())
        x = 1
        s = Screen()
        for line in lines:
            tokens = line.split()
            match tokens:
                case ["noop"]:
                    draw(x, s)
                case ["addx", val]:
                    draw(x, s)
                    draw(x, s)
                    x += int(val)
        s.print()


if __name__ == "__main__":
    p1_ans = part1("input.txt")
    print(f"part1: {p1_ans}")
    part2("input.txt")  # FJUBULRZ
