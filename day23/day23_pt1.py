# Day 23 part 1

from collections import defaultdict
import numpy as np


class Elve:

    shift = 0 # rules shifter
    instances = []
    proposed = defaultdict(lambda: []) # keys are positions, values is list of elves

    def __init__(self,pos):
        self.pos = pos # current position of this elve
        self.__class__.instances.append(self)


    def __repr__(self):
        return "<Elve at (%i,%i)>" % (self.pos.real, self.pos.imag)

    @classmethod
    def bounding_rect(cls):
        positions = [e.pos for e in cls.instances]
        r = [p.real for p in positions]
        im = [p.imag for p in positions]

        return int(min(r)), int(max(r)), int(min(im)), int(max(im))

    @classmethod
    def print_map(cls):
        min_x, max_x, min_y, max_y = cls.bounding_rect()
        final_map = np.full(((max_x-min_x+1),(max_y-min_y+1)), ".")

        positions = [e.pos for e in cls.instances]
        for p in positions:
            final_map[int(p.real) - min_x, int(p.imag) - min_y] = "#"

        mapstr = "\n".join(["".join(line) for line in np.flipud(final_map.T)])
        print(mapstr + "\n")

        return len(np.where(final_map == "#")[0]), len(np.where(final_map == ".")[0])

    def propose_move(self,new_pos):
        self.__class__.proposed[new_pos].append(self)

    def check_rule(self):

        idx = self.__class__.shift
        pos = self.pos
        other_pos = [elve.pos for elve in self.__class__.instances]

        n = pos + 1j
        s  = pos - 1j
        w  = pos -1
        e  = pos + 1

        ne = pos + 1 + 1j
        nw = pos - 1 + 1j

        se = pos + 1 - 1j
        sw = pos -1 - 1j

        rules = {
            0: ([n,ne,nw],n,"north"),
            1: ([s,se,sw],s,"south"),
            2: ([w,nw,sw],w,"west"),
            3: ([e,ne,se],e,"east")
        }


        # check if has enough space
        if all(new_pos not in other_pos for new_pos in [n,s,e,w,ne,se,nw,sw]):
            print(self,"propose no move")

        else:
            # check if can move

            if all(new_pos not in other_pos for new_pos in rules[idx % len(rules)][0]):
                self.propose_move(rules[idx % len(rules)][1])
                print(self,"propose moving", rules[idx % len(rules)][2])

            elif all(new_pos not in other_pos for new_pos in rules[(idx+1) % len(rules)][0]):
                self.propose_move(rules[(idx+1) % len(rules)][1])
                print(self,"propose moving", rules[(idx+1) % len(rules)][2])

            elif all(new_pos not in other_pos for new_pos in rules[(idx+2) % len(rules)][0]):
                self.propose_move(rules[(idx+2) % len(rules)][1])
                print(self,"propose moving", rules[(idx+2) % len(rules)][2])

            elif all(new_pos not in other_pos for new_pos in rules[(idx+3) % len(rules)][0]):
                self.propose_move(rules[(idx+3) % len(rules)][1])
                print(self,"propose moving", rules[(idx+3) % len(rules)][2])

            else:
                print(self,"propose no move2")


map = """
.....
..##.
..#..
.....
..##.
.....""".strip()


map="""
..............
..............
.......#......
.....###.#....
...#...#.#....
....#...##....
...#.###......
...##.#.##....
....#..#......
..............
..............
..............
""".strip()

with open("input.txt", "r") as file:
    map = file.read().strip()

map = map.split("\n")

# read the map
N = len(map)
p = 0 + N*1j

print(map)

for k,line in enumerate(map):
    for i,col in enumerate(line):
        if col == "#":
            p = i + (N-1 - k)*1j
            new_elve = Elve(p)

print([e.pos for e in Elve.instances])

elves = Elve.instances

"""
main program
"""
Elve.print_map()

for iter_idx in range(10):

    print("round", iter_idx)


    # first half
    elves = Elve.instances
    for elve in elves:
        elve.check_rule()

    # second half
    for new_pos,elves in Elve.proposed.items():
        if len(elves) == 1:
            elve = elves[0]
            elve.pos = new_pos

    Elve.proposed = defaultdict(lambda: [])


    # shift order
    Elve.shift += 1

    Elve.print_map()

    print("---------------")


positions = [e.pos for e in Elve.instances]
print(positions)

"""
evaluate progress
"""
n_tiles,n_empty = Elve.print_map()
print(n_empty)
