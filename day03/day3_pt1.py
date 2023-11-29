
# DAY 3


# part 1 



#lines = """
#vJrwpWtwJgWrhcsFMMfFFhFp
#jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
#PmmdzqPrVvPwwTWBwg
#wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
#ttgJtRGJQctTZtZT
#CrZsJsPPZsGzwwsLwLmpwMDw
##""".strip().split("\n")


# uncomment to use personal puzzle input

with open("input.txt", "r") as file:
    lines = file.readlines()


"""
COMP 1   | COMP 2 


ITEMS a / A
"""


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


for line in lines:

    N = int(len(line)/2)

    first_half = list( line[:N])
    second_half = list(line[N:])

    all_characters = first_half + second_half 
    all_characters = list(set(all_characters)) # get unique characters
    

    # i) find the item which is in both compartments
    for c in all_characters:


        if c in first_half and c in second_half: # have found the item

            # ii) find the ranking of the item 
            if c.isupper():
                score += priorities_upper[c]
            else:
                score += priorities[c]
            break;


print(score)
