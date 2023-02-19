import numpy as np 
import re 

class Item:

    def __init__(self,worry_level):
        self.worry_level = int(worry_level)

    def __repr__(self):
        return "<%i>" % self.worry_level

class Monkey:

    monkeys = []

    def __init__(self,starting_items,operation,test):

        self.items = starting_items
        self.operation = operation # <- function
        self.test = test  # <- triple of ints 

        self.__class__.monkeys.append(self)

        self.visited_items = set()
        self.times_inspected = 0

    def inspect_item(self,item):
        # ..

        # apply operation to item 

        self.times_inspected += 1 
        self.visited_items = self.visited_items.union(set([item]))

        log = "Monkey inspects an item with a worry level of %i\n " % item.worry_level

        old = item.worry_level
        item.worry_level = eval(self.operation)

        log += "   Worry level is modified: %s  --> %s\n" % (self.operation,item.worry_level)
        return log 


    def update_worry_level(self,item):
        # int(np.floor(x/3.))

        item.worry_level = int(np.floor(item.worry_level/3.))
        log = "   Monkey gets bored with item. divided by 3 to %i\n" % item.worry_level
        return log  

    def throw_to_monkey(self,idx):
        # throw item 
        new_monkey = self.__class__.monkeys[idx]
        item = self.items[0]

        if len(self.items) > 1:
            self.items = self.items[1:]        
        else:
            self.items = []
        
        log = "  Item with worry level %i is thrown to monkey %i\n" % (item.worry_level,idx)

        new_monkey.items.append(item)
        return log 

    def test_worry_level(self,item):
        # ..
        
        log = ""
        # apply test to item 
        if item.worry_level % int(self.test[0]) == 0:
            # throw to monkey 
            log += "   Current worry level is divisible\n"
            log += self.throw_to_monkey(self.test[1]) + "\n"
        else:
            log += "   Current worry level is not divisible\n"
            log += self.throw_to_monkey(self.test[2]) + "\n"

        return log 
       
    def update(self):

        log = ""
        for item in self.items:
            log += str(self.inspect_item(item))
            log += str(self.update_worry_level(item))
            log += str(self.test_worry_level(item))
        return log 

input = """
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
""".strip().split("\n\n")


with open("input.txt", "r") as file:
    input = file.read()

input = input.strip().split("\n\n")


for monkey in input:
    # extract information 

    infos = monkey.split("\n")
    starting = "[" + re.match( "  Starting items: (.*)",infos[1]).group(1) + "]"
    operation = re.match("  Operation: new = (.*)", infos[2]).group(1)
    test1 = int(re.match("  Test: divisible by (.*)",infos[3]).group(1))
    test2 = int(re.match("    If true: throw to monkey (.*)",infos[4]).group(1))
    test3 = int(re.match("    If false: throw to monkey (.*)",infos[5]).group(1))
    test = (test1,test2,test3)

    print(starting)
    starting_items = []
    for s in eval(starting):
        starting_items.append(Item(s))

    my_monkey = Monkey(starting_items,operation,test)


# compute rounds 
for k in range(20):
    for monkey in Monkey.monkeys:
        log = monkey.update()
        # print(log)
        # print("\n")


    for i, monkey in enumerate(Monkey.monkeys):
        print("Monkey %i" %i, monkey.items)
    print("---")


# find two most active monkeys 
for i, monkey in enumerate(Monkey.monkeys):
    print("Monkey %i inspected items %i items", monkey.times_inspected)


x = sorted([m.times_inspected for m in Monkey.monkeys])


# find level of monkey business  = multiply inspected items 
print(x[-1] * x[-2])
