class Instruction:

    def __init__(self):
        # The primary instruction code, ie CREATE, DROP, SELECT, etc...
        self.primaryInstruction = ""

        # In the event of a secondary instruction (used with ALTER)
        self.secondaryInstruction = ""

        # Attributes used by instruction code
        self.attributes = []
        
        # Table used by instruction
        self.tableUsed = ""

        # Database used by instruction (only used by USE instruction)
        self.database = ""

        # Attribute pairs define name and type of attribute, used in CREATE
        self.attrPairs = []

        # Full instructionLi
        self.instructionLine = ""

class Parser:

    def __init__(self, filename):
        self.instructions = []
        self.instructionSet = filename
        
    def print(self):
        for i in self.instructions:
            print("[{}\n primaryInstruction: {}\nsecondaryInstruction: {}\n attributes: {}\n tableUsed: {}\n database: {}\n attrPairs: {}\n".format(i.instructionLine,i.primaryInstruction, i.secondaryInstruction, i.attributes, i.tableUsed,i.database,i.attrPairs))


    # Reads file and parses instructions
    def read(self):
        f = open(self.instructionSet, 'r')

        #Read line by line
        for line in f:
            # Skip line if its a comment or blank
            if line.startswith("--") or line.isspace():
                continue
            else:
                self.parse(line) 

    # Parses line and creates instruction metadata
    def parse(self, line):

        i = Instruction()
        i.instructionLine = line
        
        if line.startswith("CREATE DATABASE"):
            i.primaryInstruction = "CREATE DATABASE"
            i.database = (line.split()[-1])[:-1]
            
        elif line.startswith("DROP DATABASE"):
            i.primaryInstruction = "DROP DATABASE"
            i.database = (line.split()[-1])[:-1]

        elif line.startswith("CREATE TABLE"):
            i.primaryInstruction = "CREATE TABLE"
            i.tableUsed = line.split()[2]
            self.parse_attr_pairs(line[line.find("("):len(line)], i) 
        elif line.startswith("DROP TABLE"):
            i.primaryInstruction = "DROP TABLE"
            i.tableUsed = (line.split()[-1])[:-1]

        elif line.startswith("SELECT"):
            i.primaryInstruction = "SELECT"

            # Check if SELECT *
            if(line.split()[1] == "*"):
                i.tableUsed = (line.split()[3])[:-1]



        elif line.startswith("USE"):
            i.primaryInstruction = "USE"
            i.instructionLine = line
            i.database = (line.split()[-1])[:-1]

        elif line.startswith("ALTER TABLE"):
            i.primaryInstruction = "ALTER TABLE"
            ls = line.split()
            i.tableUsed = ls[2]
            i.secondaryInstruction = ls[3]
            i.attrPairs.append([ls[4],(ls[5])[:-1]])
        elif line.startswith(".EXIT"):
            i.primaryInstruction = "EXIT"
        else:
            print("Instruction " + line + " is unknown :(")
        
        self.instructions.append(i)

    def parse_attr_pairs(self, attrSubstr, instruction):
        ss = attrSubstr[1:len(attrSubstr)-3]
        while len(ss) > 0:
            e = ss.find(",")
            if e < 0:
                e = len(ss)
            instruction.attrPairs.append(ss[:e].split())
            ss = (ss[ss.find(","):])[2:]




