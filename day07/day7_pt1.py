# Day 7 part 1

terminal = """
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k""".strip().split("\n")


with open("input.txt", "r") as file:
    terminal = file.readlines()


"""
{
 "/":    <- 
    {
        "a": {    <- 
            "e":
            "f":
            "g": ... 
        },
        "d": {
            "j":
            ...
        }

    }   
}
"""

# filetree = {
#     "/": None
# }


class File:

    def __init__(self,name,size):
        self.name = name 
        self.size = size 


class Folder:

    instances = []

    def __repr__(self):
        return "<%s>" % (self.name)

    def __init__(self,name,parent,create_folder=True):

        self.files = {}
        self.name = name 
        self.size = 0
        self.parent = parent # root has no parent
        self.children = {}

        if create_folder:
            self.__class__.instances.append(self)

    def add_file(self,fname,size):
        
        if fname in self.files: # O(1) lookup
            return # already there 
    
        # could not find 
        new_file = File(fname,size)
        # self.size += size 
        self.increase_size(size)

        print("new file",fname,"in directory ",self.name)
        
    def increase_size(self,size):

        parent = self

        while parent is not None:
            parent.size += size
            parent = parent.parent 

    def explore_dir(self,chdir,create_folder=True):
        
        if chdir == "..":
            # print("    -->", self.parent.name)
            return self.parent
        
        else:

            # print(" dir",chdir, "in" , self.name)
            
            if chdir in self.children:
                # exists already 
                return self.children[chdir]

            # not existent
            # folder 
            #    - new empy folder 
            #    - ...
            else:
                new_child = Folder(chdir,parent=self,create_folder=create_folder)
                return new_child 


root = Folder(name="/",parent=None)


current_dir = root 
idx = 1

while idx < len(terminal):

    new_line = terminal[idx].strip()

    print("new_line", new_line)

    if new_line.startswith("$ cd"):
        
        # change directory 

        chdir = new_line.split("$ cd")[1].strip()
        # print("change to", chdir)

        current_dir = current_dir.explore_dir(chdir)

    if new_line == "$ ls":
        # list directory
        
        has_ended = False 
        while not has_ended and idx < len(terminal)-1:
            
            idx += 1 

            new_output = terminal[idx]

            if new_output.startswith("$"):
                has_ended = True 
                idx -= 1
                break
                
            elif new_output.startswith("dir "):
                # get information about a dir 
                mydir = new_output.split("dir")[1].strip()
                _ = current_dir.explore_dir(mydir,create_folder=False)
            
            else:
                size = int(new_output.split(" ")[0])

                print("size")
                fname = new_output.split(" ")[1]
                # add file to the directory
                current_dir.add_file(fname,size)

    idx += 1



# print(Folder.instances)


sol = 0

for f in Folder.instances:
    # print(f.name,f.size)

    if f.size <= 100000:
        sol += f.size 


print("SOLUTION", sol)

# part 2 

tot_size = 70000000
required = 30000000
unused = tot_size - root.size 
print("unused",unused)

candidates = []

for f in Folder.instances:

    if f.size + unused >= required:
        candidates.append(f)

#for c in candidates:
#    print(c.name,c.size)

best = sorted(candidates,key=lambda x: x.size)[0]
print("best candidate", best,best.size)
