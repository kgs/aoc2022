from typing import Self, Callable
from dataclasses import dataclass, field


@dataclass
class Node:
    name: str
    size: int | None = None
    parent: Self | None = None
    subdirs: dict[str, Self] = field(default_factory=dict)
    files: list[Self] = field(default_factory=list)
    cached_total_size: int | None = None  # not necessary, but helpful when visiting multiple times

    def total_size(self) -> int:
        if self.cached_total_size:
            return self.cached_total_size
        files_size = sum([f.size for f in self.files])
        subdirs_size = sum([d.total_size() for d in self.subdirs.values()])
        self.cached_total_size = files_size + subdirs_size
        return self.cached_total_size


def find_dirs(n: Node, p: Callable[[Node], bool]) -> list[Node]:
    res = []
    if p(n):
        res.append(n)
    for s in n.subdirs.values():
        res += find_dirs(s, p)
    return res


def part1(input_txt: str) -> int:
    with open(input_txt) as f:
        root = Node(name="/")
        c = root
        for line in f:
            tokens = line.split()
            match tokens:
                case ["$", "cd", "/"]:
                    c = root
                case ["$", "cd", ".."]:
                    c = c.parent
                case ["$", "cd", dir_name]:
                    c = c.subdirs[dir_name]
                case ["$", "ls"]:
                    pass
                case ["dir", dir_name]:
                    d = Node(name=dir_name, parent=c)
                    c.subdirs[dir_name] = d
                case [file_size, file_name]:
                    f = Node(name=file_name, size=int(file_size), parent=c)
                    c.files.append(f)
                case _:
                    raise Exception("should not happen!")
        interesting_dirs = find_dirs(root, lambda n: n.total_size() <= 100_000)
        return sum([d.total_size() for d in interesting_dirs])


def part2(input_txt: str) -> int:
    with open(input_txt) as f:
        pass


if __name__ == "__main__":
    p1_ans = part1("input.txt")
    print(f"part1: {p1_ans}")
    p2_ans = part2("input.txt")
    print(f"part2: {p2_ans}")
