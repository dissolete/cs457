#db.py -- Defines the objects and methods for reading a database into memory
#           and writing to files
#Author - Gage Thomas, Jake Shepherd (secondary)
#Class: CS 457
#Date: 3/12/2018
#Version 1: Defines the Table and Database objects for handling the implementation
#           of commands

from parser import Instruction
import operator
import os
import sys
import copy

class Table:
    def __init__(self, tbname, dbname, exists):
        #Stores the table's name
        self.tableName = tbname
        self.dbName = dbname
        #Read in the data for the table
        self.attributeTypes = []
        self.attributeNames = []
        self.attributeValues = []#Will be a 2D list

        self.operators = { '=': operator.eq,
                           '>': operator.gt,
                           '<': operator.lt,
                           '!=': operator.ne
                         }

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
                    self.attributeValues.append(newTuple)

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

    def select(self, attributes, whereClause):
        # The results after the where filter
        results = []
        filteredResults = []
        
        # If where clause is empty, then we are simply returning every row
        if len(whereClause) == 0:
            results = copy.deepcopy(self.attributeValues)
        else:

            # Attribute that we are using in the where clause
            attributeNum = 0
            lefthandCasted = None 
            righthandCasted = None


            # Assign the attributeNum to the correct col number
            for n in range(0, len(self.attributeNames)):
                if self.attributeNames[n] == whereClause[0]:
                    attributeNum = n
                    break

            # Search through tuples
            for rowNum in range(0, len(self.attributeValues)):
                # First we have to make sure to cast the attribute
                # in question to the correct type
                # I really dont wanna check this like this, but its 
                # what im gonna do :(
                if self.attributeTypes[attributeNum] == "float":
                    lefthandCasted = float(self.attributeValues[rowNum][attributeNum])
                    righthandCasted = float(whereClause[2])
                elif self.attributeTypes[attributeNum] == "int":
                    lefthandCasted = int(self.attributeValues[rowNum][attributeNum])
                    righthandCasted = int(whereClause[2])
                else:
                    lefthandCasted = self.attributeValues[rowNum][attributeNum]
                    righthandCasted = whereClause[2]

                if self.operators[whereClause[1]](lefthandCasted, righthandCasted):
                    results.append(self.attributeValues[rowNum])

        # Now we filter what we display
        if len(attributes) == 0:
            # If not attribute names specified, this is a select *
            filteredResults = copy.deepcopy(results)
            newRow = []
            for i in range(0, len(self.attributeNames)):
                newRow.append(self.attributeNames[i] + " " + self.attributeTypes[i])
            filteredResults.insert(0, newRow)
        else:
            #first we add the column names with their type
            newRow = []
            for i in range(0, len(self.attributeNames)):
                if self.attributeNames[i] in attributes:
                    newRow.append(self.attributeNames[i] + " " + self.attributeTypes[i])
            filteredResults.append(newRow)

            # Then, we filter out all of the attributes we dont want to select

            for r in range(0, len(results)):
                newRow = []
                for c in range(0, len(results[r])):
                    
                    if self.attributeNames[c] in attributes:
                        newRow.append(results[r][c])
                filteredResults.append(newRow)

        return filteredResults

    def delete(self, whereClause):
        attributeNum = 0
        lefthandCasted = None 
        righthandCasted = None
        numRowsAffected = 0
        rowsToDelete = []
        # Assign the attributeNum to the correct col number
        for n in range(0, len(self.attributeNames)):
            if self.attributeNames[n] == whereClause[0]:
                attributeNum = n
                break

        # Search through tuples
        for rowNum in range(0, len(self.attributeValues)):
            # First we have to make sure to cast the attribute
            # in question to the correct type
            # I really dont wanna check this like this, but its 
            # what im gonna do :(
            if self.attributeTypes[attributeNum] == "float":
                lefthandCasted = float(self.attributeValues[rowNum][attributeNum])
                righthandCasted = float(whereClause[2])
            elif self.attributeTypes[attributeNum] == "int":
                lefthandCasted = int(self.attributeValues[rowNum][attributeNum])
                righthandCasted = int(whereClause[2])
            else:
                lefthandCasted = self.attributeValues[rowNum][attributeNum]
                righthandCasted = whereClause[2]
            if self.operators[whereClause[1]](lefthandCasted, righthandCasted):        
                # mark this row for deletion later
                rowsToDelete.append(rowNum)
                numRowsAffected += 1

        # delete rows that have been marked
        for n in range(0, len(rowsToDelete)):
            self.attributeValues.pop(rowsToDelete[n] - n)

        # make permanent 
        self.write_to_file()
        return numRowsAffected


#Use to insert a new tuple into the table
#Tup is a list that is the tuple that should be added
    def insert(self, tup):
        f = open(self.dbName + "/" + self.tableName + ".txt", "a")
        newTup = ""
        for attrNum in range(0, len(tup), 1):
            newTup = newTup + tup[attrNum] + " "
        self.attributeValues.append(tup)
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

    def update(self, updateAttrName, updateSetToVal, whereClause):
        # Filter attrs by where clause
        # Attribute that we are using in the where clause
        attributeNum = 0
        lefthandCasted = None 
        righthandCasted = None
        numRowsAffected = 0

        # Assign the attributeNum to the correct col number
        for n in range(0, len(self.attributeNames)):
            if self.attributeNames[n] == whereClause[0]:
                attributeNum = n
                break

        # Search through tuples
        for rowNum in range(0, len(self.attributeValues)):
            # First we have to make sure to cast the attribute
            # in question to the correct type
            # I really dont wanna check this like this, but its 
            # what im gonna do :(
            if self.attributeTypes[attributeNum] == "float":
                lefthandCasted = float(self.attributeValues[rowNum][attributeNum])
                righthandCasted = float(whereClause[2])
            elif self.attributeTypes[attributeNum] == "int":
                lefthandCasted = int(self.attributeValues[rowNum][attributeNum])
                righthandCasted = int(whereClause[2])
            else:
                lefthandCasted = self.attributeValues[rowNum][attributeNum]
                righthandCasted = whereClause[2]
            if self.operators[whereClause[1]](lefthandCasted, righthandCasted):
                for c in range(0, len(self.attributeValues[rowNum])):
                    if self.attributeNames[c] == updateAttrName:
                        self.attributeValues[rowNum][c] = updateSetToVal
                        numRowsAffected += 1

        # make permanent 
        self.write_to_file()

        return numRowsAffected

    #Used when a previously non-existent table is made to add all attributes
    #Attribute pairs is a 2D array where each row is an attribute name and
    #Its type
    def initializeAttr(self, attrPairs):
        #For each attribute, append its name and type
        for attr in attrPairs:
            self.attributeNames.append(attr[0])
            self.attributeTypes.append(attr[1])
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
            f = open(self.name + "/" + self.name + ".txt", "r")
            for line in f:
                self.tables.append(Table(line.strip(), self.name, True))
            f.close()
        else:
            self.addMetaData()

    #Used when a previously non-existent database is made or when tables
    #are dropped
    def addMetaData(self):
        f = open(self.name + "/" + self.name + ".txt", "w")
        for tb in self.tables:
            f.write(tb.tableName + "\n")
        f.close()

    #Creates a new table in this database
    #attrPairs is a 2D array, each row is an attribute name and its type
    def createTable(self, tbName, attrPairs):
        #First update the metadata file
        f = open(self.name + "/" + self.name + ".txt", "a")
        f.write(tbName + "\n")#Assuming that this creates a new line
        f.close()

        #Now, create the table
        newTable = Table(tbName, self.name, False)
        self.tables.append(newTable)
        newTable.initializeAttr(attrPairs)#Should be written to a file

    #Used to get a table
    def getTable(self, tbName):
        for tb in self.tables:
            if(tb.tableName.lower() == tbName.lower()):
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

    #Used to join and print the joined tables
    def joinTables(self, leftName, rightName, leftAlias, rightAlias, whereClause, joinType):
        leftTable = self.getTable(leftName)
        rightTable = self.getTable(rightName)
        leftCompare = 0
        rightCompare = 0

        #Get the column numbers for join comparison
        for n in range(0, len(leftTable.attributeNames)):
            if leftTable.attributeNames[n] == whereClause[0].split(".")[1]:
                leftCompare = n
                break

        for n in range(0, len(rightTable.attributeNames)):
            if rightTable.attributeNames[n] == whereClause[2].split(".")[1]:
                rightCompare = n
                break

        #Print the header
        for n in range(0, len(leftTable.attributeNames)):
            print("{} {} | ".format(leftTable.attributeNames[n], leftTable.attributeTypes[n]), end="" )
#Print the right table's header
        for n in range(0, len(rightTable.attributeNames)):
            if n != rightCompare:
                if n < (len(rightTable.attributeNames) - 1):
                    print("{} {} | ".format(rightTable.attributeNames[n], rightTable.attributeTypes[n]), end="" )
                else :
                    print("{} {}".format(rightTable.attributeNames[n], rightTable.attributeTypes[n]), end="" )
        print(" ")

        #Now join any tuples using a nested loop join, checking to see if any tuple
        #is left out on the left hand side and printing it if it is a left outer join

        for leftTuple in leftTable.attributeValues :
            wasMatched = False

            for rightTuple in rightTable.attributeValues :

                if leftTuple[leftCompare] == rightTuple[rightCompare]:
                    wasMatched = True
                    self.printTuple(leftTuple, False)
                    self.printTuple(rightTuple, True)
            if (not wasMatched) and (joinType == "left outer"):
                self.printTuple(leftTuple, False)
                self.printTuple([""] * len(rightTable.attributeNames), True)
            print(" ")

    def printTuple(self, tupleToPrint, printAllFlag):
        l = len(tupleToPrint)
        for n in range(0, l):
            print("{}|".format(tupleToPrint[n]), end='')

            if n == l - 1 and not printAllFlag:
                print(tupleToPrint[n],end='')
            elif n == l - 1:
                print(tupleToPrint[n] + "|",end='')
