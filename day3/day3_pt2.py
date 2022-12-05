
# DAY 3


# part 2

#lines = """
#vJrwpWtwJgWrhcsFMMfFFhFp
#jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
#PmmdzqPrVvPwwTWBwg
#wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
#ttgJtRGJQctTZtZT
#CrZsJsPPZsGzwwsLwLmpwMDw
#""".strip().split("\n")


# uncomment to use personal puzzle input


with open("input.txt", "r") as file:
    lines = file.readlines()

def get_next_group():
    # generator to get the next item 

    l1 = lines.pop()
    l2 = lines.pop()
    l3 = lines.pop()
    next_group = [l1,l2,l3]

    return next_group

priorities = {
    "a": 1,
    "b": 2,
    "c": 3,
    "d": 4,
    "e": 5,
    "f": 6,
    "g": 7,
    "h": 8,
    "i": 9,
    "j": 10,
    "k": 11,
    "l": 12,
    "m": 13,
    "n": 14,
    "o": 15,
    "p": 16,
    "q": 17,
    "r": 18,
    "s": 19,
    "t": 20,
    "u": 21,
    "v": 22,
    "w": 23,
    "x": 24,
    "y": 25,
    "z": 26,
}

priorities_upper = {}

for k,v in priorities.items():
    priorities_upper[k.upper()] = v + 26


score = 0 

while len(lines) > 0:

    group = get_next_group()
    print(group)

    u = group[0].strip()
    v = group[1].strip()
    w = group[2].strip()

    all_characters = list(u) + list(v) + list(w)
    all_characters = list(set(all_characters))

    for c in all_characters:

        if c in u and c in v and c in w:
            
            if c.isupper():
                score += priorities_upper[c]
            else:
                score += priorities[c]

            break;


print(score)

