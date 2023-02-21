# Day 21

input = """
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
""".strip()

with open("input.txt","r") as file:
    input = file.read().strip()



lines = input.split("\n")



class Monkey:

    instances = {}
    values = {}

    def __init__(self,code,job):

        self.code = code # e.g. ljgn

        self.wait_for = []  # wait for
        self.report_to = [] # report to

        if job is not None:
            self.assign_job(job)  # (a,b,op)

        self.__class__.instances[code] = self
        print("Create monkey", code ," op", job,self.wait_for)

    def assign_job(self,job):

        self.job = job # store job instructions

        if not isinstance(job,int) and job is not None: # modify wait for
            self.wait_for = [self.job[0] , self.job[1]]


    def check_done(self):
        val_dict = self.__class__.values
        # print(val_dict)
        if len(self.wait_for) == 0: # self.job[0] in val_dict and self.job[1] in val_dict:

            #print("        --->", self.code,"is done...")
            #print("\n")

            u = val_dict[self.job[0]]
            v = val_dict[self.job[1]]

            if self.job[2] == "-":
                val = u-v
            elif self.job[2] == "+":
                val = u+v
            elif self.job[2] == "/" :
                val = u/v
            elif self.job[2] == "*":
                val = u*v

            print( "                    ---> yell ", val)

            self.report(val)


    def report(self,val):
        print(self.code," report ", val )

        self.__class__.values[self.code.strip()] = int(val)

        for monkey in self.report_to:
            m = self.__class__.instances[monkey]
            # print("remove %s from %s 's waiting list "%(self.code,m.code))
            m.wait_for.remove(self.code)
            # print("       Monkey",m.code, "no longer waits for", self.code,"remaining:", m.wait_for)

            m.check_done()


for line in lines:

    monkey = line.split(":")[0]
    job = line.split(":")[1]
    # print("Line", line,"monkey",monkey,"job",job)

    a = None
    b = None
    op = None

    # decide if its an elementary number or a complex calculation
    if len(job.split(" + ")) > 1:
        a = job.split(" + ")[0].strip()
        b = job.split(" + ")[1].strip()
        op = (a,b,"+")

    elif len(job.split(" / ")) > 1:
        a = job.split(" / ")[0].strip()
        b = job.split(" / ")[1].strip()
        op = (a,b,"/")

    elif len(job.split(" * ")) > 1:
        a = job.split(" * ")[0].strip()
        b = job.split(" * ")[1].strip()
        op = (a,b,"*")

    elif len(job.split(" - ")) > 1:
        a = job.split(" - ")[0].strip()
        b = job.split(" - ")[1].strip()
        op = (a,b,"-")

    else:
        op = int(job )

    for m in [a,b]:
        if m not in Monkey.instances and m is not None:
            new_monkey = Monkey(m,None)

    if monkey not in Monkey.instances:
        new_monkey = Monkey(monkey,op)
    else:
        new_monkey = Monkey.instances[monkey]
        new_monkey.assign_job(op)

        # print("   --> apply job %s to monkey %s " % (op,new_monkey.code))
        # print("       .--> now %s waits for %s" % (new_monkey.code,new_monkey.wait_for))
        # print("       .--> now %s reports to %s" % (new_monkey.code,new_monkey.report_to))


    if a is not None:
        my_monkey = Monkey.instances[monkey]
        a_monkey = Monkey.instances[a]
        # my_monkey.wait_for.append(a)
        if monkey not in a_monkey.report_to:
            a_monkey.report_to.append(monkey)

    if b is not None:
        my_monkey = Monkey.instances[monkey]
        b_monkey = Monkey.instances[b]
        # my_monkey.wait_for.append(b)
        if monkey not in b_monkey.report_to:
            b_monkey.report_to.append(monkey)

for line in lines:

    monkey = line.split(":")[0]
    job = line.split(":")[1]

    a = None
    b = None
    op = None

    # decide if its an elementary number or a complex calculation
    if len(job.split(" + ")) > 1 or  len(job.split(" / ")) > 1 or  len(job.split(" * ")) > 1 or  len(job.split(" - ")) > 1:
        pass # is a complex calculation
    else:
        op = job  # < mistake here?

        my_monkey = Monkey.instances[monkey]
        my_monkey.report(eval(job)) # <- just eval the integer
