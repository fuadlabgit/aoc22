# Day 19 part 1 

# obsidian-collecting robots
# clay = lehm

# clay-collecting robots
# ore-collecting robots = 1


"""
IDEA:

Always look where the bottleneck is... 


"""


import re
import numpy as np 


input = """
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian
""".strip()


class Factory:

    def __init__(self,prodfunc):
        self.f = prodfunc # blueprint production function 

        self.capacity = {
            "clay": 0,
            "ore": 1,
            "obsidian": 0,
            "geode": 0,
            
        } # production capacity

        self.stock = {
            "clay": 0,
            "ore": 0,
            "obsidian": 0,
            "geode": 0,
            None: np.inf,
        } # stock of resources 

    def produce(self):
        # spend resources to build more 

        build_order = {
            "clay": 0 ,
            "ore": 0 ,
            "obsidian": 0, 
            "geode": 0
        }
       
        s = ""
        for k,v in self.f.items():
            # print("--->", k,v)
            if v is not None: 

                have_enough = True 

                for k2,v2 in v.items():
                    # print("       have enough",k2," for building %s robot?"%k,self.stock[k2],"/",v2)
                    if self.stock[k2] < v2: # not enough resources?
                        have_enough = False 
                # print("    ",have_enough)

                if have_enough:
                    s = "    Spend "
                    for k2,v2 in v.items():
                        self.stock[k2] -= v2
                        s+= "%s %s, " % (v2,k2)
                    s+= "    to start building a %s robot" % k + "\n"
                    build_order[k] += 1

                s+= "\n"
        
        # produce 
        for k in self.capacity.keys():
            self.stock[k] += self.capacity[k]
            if self.capacity[k] > 0:
                s+= "Produce %s %s\n" % (self.capacity[k],k)

        print(s)
        print("now you have", self.stock)

        # build ordered robots 
        for k,v in build_order.items():
            self.capacity[k] += v 
            if v > 0 :
                print("    %s robot is now ready. -> one more" % k)

input = input.split("\n")
print("INPUT LEN",len(input))

factories = []

for blueprint in input:
    lines = blueprint.split(".")

    prodfunc = {
        "ore": None ,
        "clay": None,
        "obsidian": None,
        "geode": None,
    }

    for line in lines[1:]:

        if not line.strip().startswith("Each"):
            break

        match = re.match("Each (.*) robot costs (.*) (.*) and (.*) (.*)",line.strip())

        if match is not None:
            which = match.group(1)

            a = (match.group(3))
            pa =  int(match.group(2))
            b =  (match.group(5))
            pb = int(match.group(4))
            
        else:

            match = re.match("Each (.*) robot costs (.*) (.*)",line.strip())
            which = match.group(1)

            a = (match.group(3))
            pa = int(match.group(2))
            b =  None # match.group(4)
            pb =  0 # match.group(5)
            
        prodfunc[which] = {a:pa,b:pb}

    print("prodfunc",prodfunc)
    factories.append(Factory(prodfunc))


print(factories)
print("LEN(FACTORIES)",len(factories))

fac = factories[0]

print("-----")
print(fac.f)
print("-----")

for i in range(24):
    
    print("\n")
    print("======== MINUTE %i ================" % (i+1))
    fac.produce()
    print("\n")