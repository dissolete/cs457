# parser.py -- Defines the objects and methods used for parsing the SQL statements
# Author - Jake Shepherd
# Class: CS 457
# Date: 5/8/2018
#Version 4: Adding transaction support
#This version of the parser now can interpret the beginning and end of transactions.
#Select * is now once again enabled (disabled in version 3)

#Version 3: Adding join support
#This version of the parser has additional support to identify joins and the type of
#join being done. Aliases can also be identified. Because of these two features, 
#Instruction now has several more fields to track a table to join on, the type of join,
#and the aliases of the left and right tables.

# Version 2: Defines two class objects. 
#The first is the instruction class which saves information about parsed instructions.
#This info can be used when processing the instruction.
#The second class defines the parser, which is in charge of reading the SQL commands
#and creating instructions that can be understood.
#Is now updated to handle PA2 commands

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

        # Join on this table
        self.joinTable = ""

        # Join type
        # ex
        # inner
        # left
        # right
        # left outer
        # right outer
        # full outer 
        self.joinType = ""

        # User supplied aliases for the table names
        self.leftAlias = ""
        self.rightAlias = ""

        # Database used by instruction (only used by USE instruction)
        self.database = ""

        # Attribute pairs define name and type of attribute, used in CREATE
        self.attrPairs = []
        
        # List which specifies the where clause used. The first index
        # represents the attribute, the second index represents
        # the comparison operatior, the third index represents the 
        # value of comparision.
        # IE the statement where price > 150 will create the list
        # where_clause = ['price', '>', '150']
        # and the statement where name = 'jake' will create the list
        # where_clause = ['name', '=', 'jake']
        self.whereClause = []

        # During an update statement, these two variables are used.
        # UpdateAttributeName defines what attribute is being changed
        # during the update, and updateSetToValue defines what the new
        # attribute is being set to.
        # IE the statement set name = 'Gizmo' will create the variables
        # updateAttributeName = "name"
        # updateSetToValue = "Gizmo"
        self.updateAttributeName = ""
        self.updateSetToValue = ""

        # List stores the attribute values to be inserted
        # IE, the statement
        # insert into Product values(1, 'Gizmo', 19.99)
        # will create the list
        # insertValues = ['1', 'Gizmo', '19.99']
        self.insertValues = []

        # Full instructionLi
        self.instructionLine = ""

class Parser:

    def __init__(self):
        self.singleInstruction = Instruction()
        self.joinWords = ["left", "inner", "right", "full", "outer"]
        
    # Prints the instructions generated after parsing
    # Primarily used for debug purposes
    def print(self):

            i = self.singleInstruction
            print("[{}\n primaryInstruction: {}\nsecondaryInstruction: {}\n attributes: {}\n tableUsed: {}\n database: {}\n attrPairs: {}".format(i.instructionLine,i.primaryInstruction, i.secondaryInstruction, i.attributes, i.tableUsed,i.database,i.attrPairs, end=''))
            print("whereClause: {}".format(i.whereClause, end=''))
            print("updateAttributeName: {}".format(i.updateAttributeName, end=''))
            print("updateSetToValue: {}".format(i.updateSetToValue, end=''))
            print("insertValues: {}".format(i.insertValues, end=''))
            print("joinTable: {}".format(i.joinTable))
            print("joinType: {}".format(i.joinType))
            print("left/right alias: {} {} ".format(i.leftAlias, i.rightAlias))

    # Parses line and creates instruction metadata
    # Lots of array splicing going on. Not intended to be completely readable :)
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
            i.tableUsed = line.split()[2].split('(')[0].lower()
            self.parse_attr_pairs(line[line.find("("):len(line)], i) 
            valid = True;

        elif line.lower().startswith("drop table"):
            i.primaryInstruction = "drop table"
            i.tableUsed = (line.split()[-1])[:-1].lower()
            valid = True;

        elif line.lower().startswith("select"):
            i.primaryInstruction = "select"

            if(len(line.split()) == 4):
                i.tableUsed = line.split()[3].replace(';', '')
                valid = True
                self.singleInstruction = i
                return


            # Check if SELECT *
            if(line.split()[1] != "*"):
                #fetch attrs 1 by 1 until the keywork from is found
                ws = line[7:].split()
                for k in range(0, len(ws)):
                    if ws[k] != "from":
                        i.attributes.append(ws[k].lower().replace(',', ''))
                    else:
                        # found the from keyword, parse the table names
                        # for possible joins

                        # The first table used is always after the keyword from
                        i.tableUsed = ws[k+1].replace(';', '').lower()

                        break
            else:
                i.tableUsed = line.split()[3].replace(';','').lower()

            # Finding the next table relies on two cases
            # The first is when the tables are listed
            # The second is when the join type is explicit
            # Lets look at the next word after the usr supplied name
            ws = line[line.find("from"):].split()
            
            l = 2
            word = ws[l].lower()
         
            # This word is either a tablename or a specific keyword
            # Check if it is a jon word
            if ws[l+1] in self.joinWords:
                # check we have an outer join
                if ws[l+2] == "outer":      
                    # cool so the join is a combo of the
                    # first join word and this outer
                    i.joinType = ws[l+1].lower() + " " + ws[l+2]
                    # then i + 3 is the word 'join' and i + 4 is the join table name
                    i.joinTable = ws[l+4]

                    # get right alias
                    i.rightAlias = ws[l+5]
                else:
                    # here there is no "outer" join, then the join type is just ws[i]
                    i.joinType = ws[l+1].lower()
                    # and the join table is i + 3
                    i.joinTable = ws[l+3]

                    # get right alias
                    i.rightAlias= ws[l+4]


            else:
                # Otherwise, the tables are listed
                i.joinTable = ws[l+1]
                i.joinType = "inner"
                i.rightAlias = ws[l+2]

            i.leftAlias = ws[l].replace(',', '')
            # look for the where keyword or the on keyword
            # these two are parsed the same
            ws = line[line.find("where"):]
            
            # if the length of ws is 0, then the where clause was not found
            # and so the on keyword is probably used

            if len(ws) <= 1:
                ws = line[line.find("on"):]

            # now parse the thing
            self.parse_where_clauses(ws, i)
                

            valid = True;

        elif line.lower().startswith("use"):
            i.primaryInstruction = "use"
            i.instructionLine = line
            i.database = (line.split()[-1])[:-1]

            valid = True;
        elif line.lower().startswith("alter table"):
            i.primaryInstruction = "alter table"
            ls = line.split()
            i.tableUsed = ls[2].lower()
            i.secondaryInstruction = ls[3]
            i.attrPairs.append([ls[4],(ls[5])[:-1]])
            valid = True;
        elif line.lower().startswith("update"):
            i.primaryInstruction = "update"
            ls = line.split()
            i.tableUsed = ls[1].lower()
            ws = line[line.find("where"):]
            us = line[line.find("set"):]
            self.parse_where_clauses(ws, i)
            self.parse_update_clause(us, i)

            valid = True
        elif line.lower().startswith("delete"):
            i.primaryInstruction = "delete"
            ls = line.split()
            i.tableUsed = ls[2].lower()
            ws = line[line.find("where"):]
            self.parse_where_clauses(ws, i)
            valid = True
        elif line.lower().startswith("insert"):
            i.primaryInstruction = "insert"
            ls = line.split()
            i.tableUsed = ls[2].lower()
            vs = line[line.find("values"):]
            self.parse_values(vs, i)
            valid = True


        elif line.lower().startswith(".exit"):
            i.primaryInstruction = "exit"
            valid = True;
        elif line.lower().startswith("begin"):
            i.primaryInstruction = "begin"
            valid = True
        elif line.lower().startswith("commit;"):
            i.primaryInstruction = "commit"
            valid = True

        if valid:
            self.singleInstruction = i

    # method parses the attributes defined in the CREATE TABLE command
    # Could also be used whenever (attr datatype, ...) is needed to be parsed
    # Again, magic array splicing
    def parse_attr_pairs(self, attrSubstr, instruction):
        ss = attrSubstr[1:len(attrSubstr)-2]
        while len(ss) > 0:
            e = ss.find(",")
            if e < 0:
                e = len(ss) 
            instruction.attrPairs.append(ss[:e].split())
            ss = (ss[ss.find(","):])[2:]

    def parse_where_clauses(self, whereLine, instruction):
        parts = whereLine.replace('\'', '').replace(';', '').split()
        if len(parts) > 0:
            instruction.whereClause.append(parts[1])
            instruction.whereClause.append(parts[2])
            instruction.whereClause.append(parts[3])

    def parse_update_clause(self, updateLine, instruction):
        parts = updateLine.replace('\'', '').replace(';', '').split()
        instruction.updateAttributeName = parts[1]
        instruction.updateSetToValue = parts[3]

    def parse_values(self, valuesLine, instruction):
        parts = valuesLine[6:].replace('(', '').replace(')', '').replace('\'', '').replace(' ', '').replace(';', '').split(',')
        instruction.insertValues = parts
