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

    def __init__(self, usingFile, filename=""):
        self.instructions = []
        self.singleInstruction = Instruction()
        self.instructionSet = filename
        self.usingFile = usingFile

        
    def print(self):
        if self.usingFile:
            for i in self.instructions:
                print("[{}\n primaryInstruction: {}\nsecondaryInstruction: {}\n attributes: {}\n tableUsed: {}\n database: {}\n attrPairs: {}\n".format(i.instructionLine,i.primaryInstruction, i.secondaryInstruction, i.attributes, i.tableUsed,i.database,i.attrPairs))

        else:
            i = self.singleInstruction
            print("[{}\n primaryInstruction: {}\nsecondaryInstruction: {}\n attributes: {}\n tableUsed: {}\n database: {}\n attrPairs: {}\n".format(i.instructionLine,i.primaryInstruction, i.secondaryInstruction, i.attributes, i.tableUsed,i.database,i.attrPairs))

    # Reads file and parses instructions
    def read(self, inputLine="--"):
        if self.usingFile:
            f = open(self.instructionSet, 'r')

            #Read line by line
            for line in f:
                # Skip line if its a comment or blank
                if line.startswith("--") or line.isspace():
                    continue
                else:
                    self.parse(line) 
        else:
            if not inputLine.startswith("--") and not inputLine.isspace():
                self.parse(inputLine)




    # Parses line and creates instruction metadata
    def parse(self, line):

        i = Instruction()
        i.instructionLine = line
        valid = False;
        
        if line.lower().startswith("create database"):
            i.primaryInstruction = "create database"
            i.database = (line.split()[-1])[:-1]
            valid = True;
            
        elif line.lower().startswith("drop database"):
            i.primaryInstruction = "drop database"
            i.database = (line.split()[-1])[:-1]
            valid = True;

        elif line.lower().startswith("create table"):
            i.primaryInstruction = "create table"
            i.tableUsed = line.split()[2]
            self.parse_attr_pairs(line[line.find("("):len(line)], i) 
            valid = True;
        elif line.lower().startswith("drop table"):
            i.primaryInstruction = "drop table"
            i.tableUsed = (line.split()[-1])[:-1]
            valid = True;

        elif line.lower().startswith("select"):
            i.primaryInstruction = "select"

            # Check if SELECT *
            if(line.split()[1] == "*"):
                i.tableUsed = (line.split()[3])[:-1]

            valid = True;


        elif line.lower().startswith("use"):
            i.primaryInstruction = "use"
            i.instructionLine = line
            i.database = (line.split()[-1])[:-1]

            valid = True;
        elif line.lower().startswith("alter table"):
            i.primaryInstruction = "alter table"
            ls = line.split()
            i.tableUsed = ls[2]
            i.secondaryInstruction = ls[3]
            i.attrPairs.append([ls[4],(ls[5])[:-1]])
            valid = True;
        elif line.lower().startswith(".exit"):
            i.primaryInstruction = "exit"
            valid = True;

        if valid and self.usingFile: 
            self.instructions.append(i)
        elif valid and not self.usingFile:
            self.singleInstruction = i

    def parse_attr_pairs(self, attrSubstr, instruction):
        ss = attrSubstr[1:len(attrSubstr)-3]
        while len(ss) > 0:
            e = ss.find(",")
            if e < 0:
                e = len(ss)
            instruction.attrPairs.append(ss[:e].split())
            ss = (ss[ss.find(","):])[2:]




