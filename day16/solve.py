from dataclasses import dataclass, field
from typing import Iterable
import re

INF = 1_000_000_000


@dataclass
class Graph:
    size: int = 0
    valve2num: dict[str, int] = field(default_factory=dict)
    flow_rate: list[int] = field(default_factory=list)
    neighbours: list[list[int]] = field(default_factory=list)
    dist: list[list[int]] = field(init=False)

    def get_valve_num(self, valve: str):
        if valve not in self.valve2num:
            self.valve2num[valve] = self.size
            self.size += 1
            self.flow_rate.append(0)
            self.neighbours.append([])
        return self.valve2num[valve]

    def add_node(self, src_node: str, flow_rate: int, dst_nodes: list[str]):
        x = self.get_valve_num(src_node)
        self.flow_rate[x] = flow_rate
        self.neighbours[x] = [self.get_valve_num(node_str) for node_str in dst_nodes]

    def calc_dist(self):
        n = self.size
        dist = [[INF] * n for _ in range(n)]
        for i in range(n):
            for j in self.neighbours[i]:
                dist[i][j] = 1
        for i in range(n):
            dist[i][i] = 0
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    x = dist[i][k] + dist[k][j]
                    if dist[i][j] > x:
                        dist[i][j] = x
        self.dist = dist


def build_graph(input_txt: str) -> Graph:
    with open(input_txt) as f:
        g = Graph()
        lines = map(lambda v: v.strip(), f.readlines())
        for line in lines:
            match = re.match(r"Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z, ]+)", line)
            src_node, flow_rate, dst_nodes = match.group(1), int(match.group(2)), match.group(3).split(", ")
            g.add_node(src_node, flow_rate, dst_nodes)
        g.calc_dist()
        return g


def gen_paths(g: Graph, node: int, time_left: int, to_visit: set[int], curr_path: list[int]) -> Iterable[list[int]]:
    for next_node in to_visit:
        time_cost = g.dist[node][next_node] + 1
        if time_cost < time_left:
            for p in gen_paths(g,
                               next_node,
                               time_left - time_cost,
                               to_visit - {next_node},
                               curr_path + [next_node]):
                yield p
    yield curr_path


def simulate(g: Graph, path: list[int], minutes: int) -> int:
    curr_node = g.valve2num["AA"]
    res = 0
    for node in path:
        minutes -= (g.dist[curr_node][node] + 1)
        res += g.flow_rate[node] * minutes
        curr_node = node
    return res


def part1(input_txt: str) -> int:
    g = build_graph(input_txt)
    nodes_to_visit = {i for i, fr in enumerate(g.flow_rate) if fr > 0}
    best = 0
    for path in gen_paths(g, g.valve2num["AA"], 30, nodes_to_visit, []):
        best = max(best, simulate(g, path, 30))
    return best


def part2(input_txt: str) -> int:
    g = build_graph(input_txt)
    nodes_to_visit = {i for i, fr in enumerate(g.flow_rate) if fr > 0}
    paths = gen_paths(g, g.valve2num["AA"], 26, nodes_to_visit, [])
    best = 0
    return best


if __name__ == "__main__":
    sample_p1_ans = part1("sample.txt")
    assert sample_p1_ans == 1651
    print(f"sample1: {sample_p1_ans}")
    p1_ans = part1("input.txt")
    assert p1_ans == 1915
    print(f"part1: {p1_ans}")
    sample_p2_ans = part2("sample.txt")
    print(f"sample2: {sample_p2_ans}")
    # p2_ans = part2("input.txt", 600_000_000)
    # print(f"part2: {p2_ans}")
