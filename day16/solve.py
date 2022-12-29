from dataclasses import dataclass, field
from datetime import datetime
import random
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


def simulate(g: Graph, nodes: list[tuple[int, int]], minutes: int) -> int:
    curr_node = g.valve2num["AA"]
    res = 0
    for fr, i in nodes:
        # move there and open valve
        minutes -= (g.dist[curr_node][i] + 1)
        if minutes <= 0:
            break
        res += fr * minutes
        curr_node = i
    return res


def part1(input_txt: str, iterations: int) -> int:
    g = build_graph(input_txt)
    nodes = [(g.flow_rate[i], i) for i in range(g.size) if g.flow_rate[i] > 0]
    best = 0
    for it in range(iterations):
        if it % (iterations / 100) == 0:
            print("{} {:.2f}% {}".format(datetime.now(), it * 100 / iterations, best))
        best = max(best, simulate(g, nodes, 30))
        random.shuffle(nodes)
    return best


def part2(input_txt: str, iterations: int) -> int:
    g = build_graph(input_txt)
    nodes = [(g.flow_rate[i], i) for i in range(g.size) if g.flow_rate[i] > 0]
    best = 0
    for it in range(iterations):
        if it % (iterations / 100) == 0:
            print("{} {:.2f}% {}".format(datetime.now(), it * 100 / iterations, best))
        for i in range(len(nodes)):
            best = max(best, simulate(g, nodes[:i], 26) + simulate(g, nodes[i:], 26))
        random.shuffle(nodes)
        # TODO: instead of random shuffle, generate only possible paths in which nodes could be visited in time
    return best


if __name__ == "__main__":
    # sample_p1_ans = part1("sample.txt", 100_000)
    # print(f"sample1: {sample_p1_ans}")
    # p1_ans = part1("input.txt", 100_000_000)
    # print(f"part1: {p1_ans}")
    sample_p2_ans = part2("sample.txt", 100_000)
    print(f"sample2: {sample_p2_ans}")
    p2_ans = part2("input.txt", 600_000_000)
    print(f"part2: {p2_ans}")
