from pydantic.dataclasses import dataclass
from dataclasses import field
from collections import deque, defaultdict

DIRS = {
    "N": (0, -1),
    "E": (1, 0),
    "S": (0, 1),
    "W": (-1, 0),
    "NE": (1, -1),
    "NW": (-1, -1),
    "SW": (-1, 1),
    "SE": (1, 1)
}

POS_TO_CHECK = {
    "N": [DIRS["N"], DIRS["NE"], DIRS["NW"]],
    "S": [DIRS["S"], DIRS["SE"], DIRS["SW"]],
    "W": [DIRS["W"], DIRS["NW"], DIRS["SW"]],
    "E": [DIRS["E"], DIRS["NE"], DIRS["SE"]],
}


@dataclass
class Elf:
    x: int
    y: int


@dataclass
class Map:
    taken: set[tuple[int, int]] = field(default_factory=set)
    elves: list[Elf] = field(default_factory=list)

    def is_taken(self, p: tuple[int, int]) -> bool:
        return p in self.taken

    def move(self, e: Elf, where: tuple[int, int]):
        # it should be already on list of elves
        self.taken.remove((e.x, e.y))
        e.x, e.y = where
        self.taken.add(where)


def parse_map(input_txt: str) -> Map:
    with open(input_txt) as f:
        lines = map(lambda x: x.strip(), f.readlines())
        elves = [Elf(x, y) for y, line in enumerate(lines) for x, val in enumerate(line) if val == "#"]
        taken = {(e.x, e.y) for e in elves}
        return Map(taken, elves)


def print_map(m: Map):
    ax = [elf.x for elf in m.elves]
    ay = [elf.y for elf in m.elves]
    for y in range(min(ay) - 1, max(ay) + 2):
        line = ""
        for x in range(min(ax) - 1, max(ax) + 2):
            if (x, y) in m.taken:
                line += "#"
            else:
                line += "."
        print(line)
    print("\n\n")


def solve(input_txt: str) -> (int, int):
    res_part1, res_part2 = 0, 0

    m = parse_map(input_txt)
    proposed_dirs = deque(["N", "S", "W", "E"])

    round_no = 0
    somebody_moved = True
    while somebody_moved:
        somebody_moved = False
        round_no += 1
        next_pos = defaultdict(lambda: list())  # from position to list of elves who want it

        for elf in m.elves:
            # first check if elf can move
            can_move = False
            for d in DIRS.values():
                new_pos = (elf.x + d[0], elf.y + d[1])
                if m.is_taken(new_pos):
                    can_move = True
                    break
            if not can_move:
                continue

            # then propose move
            for pd in proposed_dirs:
                can_move = True
                for pos in POS_TO_CHECK[pd]:
                    new_pos = (elf.x + pos[0], elf.y + pos[1])
                    if m.is_taken(new_pos):
                        can_move = False

                if can_move:
                    somebody_moved = True
                    pos = (elf.x + DIRS[pd][0], elf.y + DIRS[pd][1])
                    next_pos[pos].append(elf)
                    break

        # then iterate over next_post and move only when only one elf wants there
        for pos, elves in next_pos.items():
            if len(elves) == 1:
                m.move(elves[0], pos)

        # rotate proposed dirs
        tmp = proposed_dirs.popleft()
        proposed_dirs.append(tmp)

        if round_no == 10:
            ax = [elf.x for elf in m.elves]
            ay = [elf.y for elf in m.elves]
            rect_area = (max(ax) - min(ax) + 1) * (max(ay) - min(ay) + 1)
            res_part1 = rect_area - len(m.elves)

    res_part2 = round_no
    return res_part1, res_part2


if __name__ == "__main__":
    sample_p1_ans, _ = solve("sample.txt")
    print(f"sample: {sample_p1_ans}")
    p1_ans, p2_ans = solve("input.txt")
    print(f"part1: {p1_ans}")
    print(f"part2: {p2_ans}")
