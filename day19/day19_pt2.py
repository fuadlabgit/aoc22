# Day 19 part 1

# obsidian-collecting robots
# clay = lehm

# clay-collecting robots
# ore-collecting robots = 1

import re
import numpy as np


def dfs(state,verbose=False):
    # search for a better solution

    if state in cache:
        return cache[state]

    n_ore, n_clay, n_obsidian, n_geode, q_ore, q_clay, q_obsidian, q_geode, time = state

    robots = {"ore": n_ore, "clay": n_clay, "obsidian": n_obsidian, "geode": n_geode}
    resources = {"ore": q_ore, "clay": q_clay, "obsidian": q_obsidian, "geode": q_geode}

    T = 32

    if time >= T:
        return q_geode

    maxval = 0 # number of geodes produced

    """
    simplest solution: build nothing and wait until time is up
    """

    maxval = resources["geode"] + robots["geode"] * (T-time)

    """
    Evaluate options
    """

    for option in ["ore", "clay", "obsidian", "geode"]:

        # make temporary state dicts
        eval_robots = robots.copy()
        eval_resources = resources.copy()

        if eval_robots[option] >= maxspend[option] and option != "geode":
            continue

        # 1. check requirements and wait until met
        can_build = False
        eval_time = time

        #print("option", option)
        success = False

        while (not can_build) and eval_time < T:

            # can already build?
            can_build = True
            for res_type in costs[option].keys():
                if eval_resources[res_type] < costs[option][res_type]:
                    can_build = False

            if can_build: # actually spend resources to build
                for res_type in costs[option].keys():
                    eval_resources[res_type] -= costs[option][res_type]
                success = True

            # meanwhile produce resources
            for k,v in eval_resources.items():
                eval_resources[k] += eval_robots[k] # each robot produces one unit

            eval_time += 1

        # finally build the new robot
        if success:
            # print("  > success")
            eval_robots[option] += 1

        """
        PART 2 make the cache space smaller by cropping the amotuns
        """

        for k,v in eval_resources.items():
            eval_resources[k] = min(eval_resources[k], maxspend[k] * (T-eval_time))

        # define new state
        n_ore, n_clay, n_obsidian, n_geode = eval_robots.values()
        q_ore, q_clay, q_obsidian, q_geode = eval_resources.values()

        new_state = (n_ore, n_clay, n_obsidian, n_geode, q_ore, q_clay, q_obsidian, q_geode, eval_time)
        new_val = dfs(new_state)

        # print("    ", new_val)
        maxval = max(maxval,new_val)

    cache[state] = maxval
    return maxval

"""
read the blueprint
"""

input = """
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
""".strip()


with open("input.txt", "r") as file:
    input = file.read()
input = input.strip()

lines = input.split("\n")
lines = lines[0:3]


def info_to_dict(info):
    m = re.match("Each ore robot costs (.*) ore. Each clay robot costs (.*) ore. Each obsidian robot costs (.*) ore and (.*) clay. Each geode robot costs (.*) ore and (.*) obsidian.",info)

    cost_dict = {
    "ore": {"ore": int(m.group(1))},
    "clay": {"ore": int(m.group(2))},
    "obsidian": {"ore": int(m.group(3)), "clay": int(m.group(4))},
    "geode": {"ore": int(m.group(5)), "obsidian": int(m.group(6))}
    }

    return cost_dict

agg_quality_level = 0

for idx_blueprint, line in enumerate(lines):

    robots = {
        "ore": 1,
        "clay": 0 ,
        "obsidian": 0 ,
        "geode": 0
    }

    resources = {
        "ore": 0,
        "clay": 0 ,
        "obsidian": 0 ,
        "geode": 0
    }

    cache = {}


    print("BLUEPRINT", idx_blueprint)
    # read new cost
    info = line.split(": ")[1]
    costs = info_to_dict(info)

    # compute number of geodes producable
    maxspend = {"ore": 0, "clay": 0 , "obsidian": 0, "geode": np.inf}
    for k,v in costs.items():
        for r, q in v.items():
            if r != "geode":
                maxspend[r]  = max(maxspend[r], q)

    print("maxspend", maxspend)

    n_ore,n_clay,n_obsidian,n_geode = robots.values()
    q_ore,q_clay,q_obsidian,q_geode = resources.values()

    start_state = (n_ore, n_clay, n_obsidian, n_geode, q_ore, q_clay, q_obsidian, q_geode, 0)
    res = dfs(start_state,verbose=False)
    print("geodes:", res)

    agg_quality_level += res # * (1 + idx_blueprint )


print("ANSWER", agg_quality_level)
