#db.py -- Defines the objects and methods for reading a database into memory
#           and writing to files
#Author - Gage Thomas
#Class: CS 457
#Date: 3/12/2018
#Version 1: Defines the Table and Database objects

from parser import Instruction

class Table:
    def __init__(self, tbname, dbname, exists):
        #Stores the table's name
        self.tableName = tbname
        self.dbName = dbname
        #Read in the data for the table
        self.attributeTypes = []
        self.attributeNames = []
        self.attributeValues = []#Will be a 2D list

#If the table already exists, read in the data
        if exists :

            lineNum = 0
            f = open(self.dbName + "/" + self.tableName + ".txt", "r")
            for line in f:

                theLine = line.split()

                if lineNum == 0:
                    #read in the attribute names and types 
                    for index in range(0, len(theLine), 2):
                        self.attributeNames.append(theLine[index])
                        self.attributeTypes.append(theLine[index + 1])
                else:
                    newTuple = []
                    #If not the first line, read in the actual values
                    for attributeNum in range(0, len(theLine), 1):
                        newTuple.append(theLine[attributeNum])#append each attr to the tuple
                    attributeValues.append(newTuple)

                lineNum += 1
            f.close()

#Use after any modification other than insert
    def write_to_file(self):
        f = open(self.dbName + "/" + self.tableName + ".txt", 'w')
        nextLine = ""

        #Print all the attribute names and types
        for index in range(0, len(self.attributeNames), 1): 
            nextLine = nextLine + self.attributeNames[index] + " " + self.attributeTypes[index]
            nextLine += " "

        f.write(nextLine + "\n")
        #Print all of the data
        for tupleNum in range(0, len(self.attributeValues), 1):
            nextLine = ""

            for attributeNum in range(0, len(self.attributeValues[tupleNum]), 1):
                nextLine = nextLine + self.attributeValues[tupleNum][attributeNum]
                nextLine += " "

            f.write(nextLine + "\n")
        f.close()

#Use to insert a new tuple into the table
#Tup is a list that is the tuple that should be added
    def insert_tuple(self, tup):
        f = open(self.dbName + "/" + self.tableName + ".txt", "a")
        newTup = ""
        for attrNum in range(0, len(tup), 1):
            newTup = newTup + tup[attrNum] + " "
        f.write(newTup + "\n")
        f.close()

#Alter the table by adding a new attribute, sets its value to "NULL"
#For each existing tuple, writes result to file
    def alter(self, newName, newType):
        self.attributeNames.append(newName)
        self.attributeTypes.append(newType)

        #Now add all the NULL values for the new attribute
        for tupleNum in range(0, len(self.attributeValues), 1):
            self.attributeValues[tupleNum].append("NULL")
        self.write_to_file()

    #Used when a previously non-existent table is made to add all attributes
    def initializeAttr(self, names, types):
        for index in range(0, len(names), 1):
            self.attributeNames.append(names[index])
            self.attributeTypes.append(types[index])
        self.write_to_file()

    #Need to add select, modify, and delete commands
    #Need to add PA2 commands

class DB:
    #Must specify name of the database and if it already exists
    #or if it is being created
    def __init__(self, theName, exists):
        self.name = theName
        self.tables = []#list of table objects

#If the database already exists, read in all of its data
#NEED TO CREATE A METADATA FILE IN THE DIRECTORY OF THE DATABASE
#Assuming it will be called <dbname>.txt inside the working directory
#Assuming it will be the table names on each row
        if exists:
            f = open(self.name + "/" + self.name ".txt", "r")
            for line in f:
                self.tables.append(Table(line.strip(), self.name, True))
            f.close()
        else:
            self.addMetaData()

    #Used when a previously non-existent database is made or when tables
    #are dropped
    def addMetaData(self):
        f = open(self.name + "/" + self.name ".txt", "w")
        for tb in self.tables:
            f.write(tb.tableName)
        f.close()

    #Creates a new table in this database
    def createTable(self, tbName, names, types):
        #First update the metadata file
        f = open(self.name + "/" + self.name ".txt", "a")
        f.write(tbname + ".txt")#Assuming that this creates a new line
        f.close()

        #Now, create the table
        newTable = Table(tbname, self.name, False)
        self.tables.append(newTable)
        newTable.initializeAttr(names, types)#Should be written to a file

    #Used to get a table
    def getTable(self, tbName):
        for tb in self.tables:
            if(tb.tableName == tbName):
                return tb
        return None

#Used to drop a single table
    def dropTable(self, tbName):
        index = 0
        for tb in self.tables:
            if(tb.tableName == tbName):
                del self.tables[index]
            index += 1

        #Now remove the table file
        os.remove(self.name + "/" + tbName + ".txt")
        #Now update the metadata file
        self.addMetaData()

    #Drop databases using db_manager
