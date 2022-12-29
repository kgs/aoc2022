from dataclasses import dataclass
from typing import Self
from collections import deque
import re


@dataclass
class Blueprint:
    id: int
    ore_r_cost_ore: int
    clay_r_cost_ore: int
    obs_r_cost_ore: int
    obs_r_cost_clay: int
    geo_r_cost_ore: int
    geo_r_cost_obs: int

    @classmethod
    def from_str(cls, s: str) -> Self:
        i, ore_r_cost_ore, clay_r_cost_ore, obs_r_cost_ore, \
            obs_r_cost_clay, geo_r_cost_ore, geo_r_cost_obs = map(int, re.findall(r"\d+", s))
        return cls(i, ore_r_cost_ore, clay_r_cost_ore, obs_r_cost_ore,
                   obs_r_cost_clay, geo_r_cost_ore, geo_r_cost_obs)


def solve(b: Blueprint, minutes: int) -> int:
    best = 0
    max_ore_cost = max(b.ore_r_cost_ore, b.clay_r_cost_ore, b.obs_r_cost_ore, b.geo_r_cost_ore)
    max_clay_cost = b.obs_r_cost_clay
    max_obs_cost = b.geo_r_cost_obs
    # ore, clay, obs, geo, ore_r, clay_r, obs_r, geo_r, minute
    state = (0, 0, 0, 0, 1, 0, 0, 0, minutes)
    q = deque([state])
    seen = set()
    steps = 0
    while q:
        state = q.pop()  # DFS, try to find high bests ASAP to make pruning work

        steps += 1
        if steps % 1_000_000 == 0:
            print(b.id, steps, state, len(q), len(seen), best)

        ore, clay, obs, geo, ore_r, clay_r, obs_r, geo_r, m_left = state

        # prune! no chance to beat current best even if max theoretical geo
        # will be produced in every minute left
        if geo + m_left * geo_r + (m_left - 1) * m_left // 2 < best:
            continue

        if state in seen:
            continue
        seen.add(state)

        best = max(geo, best)
        if m_left == 0:
            continue

        # produce minerals
        q.append((ore + ore_r, clay + clay_r, obs + obs_r, geo + geo_r,
                  ore_r, clay_r, obs_r, geo_r, m_left - 1))

        # buy robots (only if consumption can keep up)
        if b.ore_r_cost_ore <= ore and ore_r < max_ore_cost:  # ore_r
            q.append((ore - b.ore_r_cost_ore + ore_r, clay + clay_r, obs + obs_r, geo + geo_r,
                      ore_r + 1, clay_r, obs_r, geo_r, m_left - 1))
        if b.clay_r_cost_ore <= ore and clay_r < max_clay_cost:  # clay_r
            q.append((ore - b.clay_r_cost_ore + ore_r, clay + clay_r, obs + obs_r, geo + geo_r,
                      ore_r, clay_r + 1, obs_r, geo_r, m_left - 1))
        if b.obs_r_cost_ore <= ore and b.obs_r_cost_clay <= clay and obs_r < max_obs_cost:  # obs_r
            q.append((ore - b.obs_r_cost_ore + ore_r, clay - b.obs_r_cost_clay + clay_r, obs + obs_r, geo + geo_r,
                      ore_r, clay_r, obs_r + 1, geo_r, m_left - 1))
        if b.geo_r_cost_ore <= ore and b.geo_r_cost_obs <= obs:  # geo_r
            q.append((ore - b.geo_r_cost_ore + ore_r, clay + clay_r, obs - b.geo_r_cost_obs + obs_r, geo + geo_r,
                      ore_r, clay_r, obs_r, geo_r + 1, m_left - 1))
    return best


def part1(input_txt: str) -> int:
    with open(input_txt) as f:
        lines = map(lambda x: x.strip(), f.readlines())
        blueprints = [Blueprint.from_str(l) for l in lines]
        res = 0
        for b in blueprints:
            v = solve(b, 24)
            print(b.id, v)
            res += b.id * v
        return res


def part2(input_txt: str) -> int:
    with open(input_txt) as f:
        lines = map(lambda x: x.strip(), f.readlines())
        blueprints = [Blueprint.from_str(l) for l in lines]
        res = 1
        for b in blueprints[:3]:
            v = solve(b, 32)
            print(b.id, v)
            res *= v
        return res


if __name__ == "__main__":
    sample_p1_ans = part1("sample.txt")
    print(f"sample1: {sample_p1_ans}")
    p1_ans = part1("input.txt")
    print(f"part1: {p1_ans}")
    sample_p2_ans = part2("sample.txt")
    print(f"sample2: {sample_p2_ans}")
    p2_ans = part2("input.txt")
    print(f"part2: {p2_ans}")
